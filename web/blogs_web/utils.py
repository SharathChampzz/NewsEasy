import time
import requests
import sqlite3
from bs4 import BeautifulSoup
from typing import List, Dict
from backend.blogs_api.models import Blog
import json
from lxml import html
from .text_summarizer import Summarizer

import logging
logger = logging.getLogger('scheduler')

class News:
    def __init__(self, num_news: int = 5):
        self.num_news = num_news
        self.init_db()
        self.seen_news = self.load_seen_news()
        self.india_today_base_url = "https://www.indiatoday.in"
        self.india_express_base_url = "https://indianexpress.com/"

    def init_db(self):
        """Initialize the SQLite database to store seen and failed news."""
        self.conn = sqlite3.connect('news_db.sqlite')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY,
                title TEXT UNIQUE,
                status BOOLEAN
            )
        ''')
        self.conn.commit()

    def load_seen_news(self) -> set:
        """Load previously seen news titles from the SQLite database."""
        self.cursor.execute('SELECT title FROM news WHERE status = 1')
        return set(row[0] for row in self.cursor.fetchall())

    def save_news(self, title: str, status: bool):
        """Save news titles with their status to the SQLite database."""
        try:
            logger.info(f'Saving news to local database: {title}, status={status}')
            self.cursor.execute('INSERT INTO news (title, status) VALUES (?, ?)', (title, status))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass  # Ignore duplicates

    def fetch_india_today_news(self) -> List[Dict[str, str]]:
        base_url = self.india_today_base_url
        logger.info(f'fetch_india_today_news: Fetching all news from {base_url}...')
        response = requests.get(base_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.select('.B1S3_story__card__A_fhi .B1S3_content__thumbnail__wrap__iPgcS .B1S3_story__thumbnail___pFy6 a')

        news_data = []
        count = 0
        for post in elements:
            if count >= self.num_news:
                break
            post_url = f"{base_url}{post.get('href')}"
            title = post.get('title')

            if title in self.seen_news:
                continue

            try:
                child_image_src = post.find('img').get('src')
                logger.info(f'fetch_india_today_news: Fetching news details from {post_url}...')
                news_details = requests.get(post_url)
                news_details.raise_for_status()
                news_soup = BeautifulSoup(news_details.text, 'html.parser')
                news_highlights = news_soup.select('ul.Story_highlights__list__FRRjs li')
                highlights_text = [highlight.get_text() for highlight in news_highlights]

                news_data.append({
                    'title': title,
                    'posturl': post_url,
                    'image': child_image_src.split('&size=')[0],
                    'highlights': '<br>'.join(highlights_text)
                })

                self.seen_news.add(title)
                self.save_news(title, True)
                count += 1
                logger.info(f'fetch_india_today_news: To avoid bot detection, sleeping for 60 seconds...')
                time.sleep(60)

            except Exception as e:
                logger.info(f"Error processing news: {title}. Error: {e}")
                self.save_news(title, False)
                continue

        return news_data

    def scrape_links(self, url, xpaths):
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        webpage_content = response.content

        # Parse the webpage content with lxml
        tree = html.fromstring(webpage_content)

        # Extract links and titles for each XPath
        links_with_titles = []
        for xpath in xpaths:
            elements = tree.xpath(xpath)
            for element in elements:
                href = element.get('href')
                title = element.text_content().strip()
                if href and title:
                    links_with_titles.append((title, href))

        return links_with_titles

    def fetch_india_express_news(self) -> List[Dict[str, str]]:
        links_with_titles = self.scrape_links(self.india_express_base_url, [
            "//*[@class='other-article ']//*[@class='content-txt']//h3//a",
            "//*[@class='top-news']//h3//a"
        ]) # this will give latest top news from indian express
        
        count = 0
        news_data = []
        for title, link in links_with_titles:
            try:
                if count >= self.num_news:
                    break
                news_details = self.__scrape_script_tag_india_express(link)
                if news_details:
                    news_data.append(news_details)
                    self.seen_news.add(title)
                    self.save_news(title, True)
                    count += 1
                    logger.info(f'fetch_india_express_news: To avoid bot detection, sleeping for 60 seconds...')
                    time.sleep(60)
            except Exception as e:
                logger.info(f"Error processing news: {link}. Error: {e}")
                self.save_news(title, False)
                continue
            
        return news_data
        
    def __scrape_script_tag_india_express(self, news_details_page_url: str):
        # Fetch the webpage content
        response = requests.get(news_details_page_url)
        response.raise_for_status()  # Check if the request was successful
        webpage_content = response.text

        # Parse the webpage content with BeautifulSoup
        soup = BeautifulSoup(webpage_content, 'html.parser')

        # Find all <script> tags
        script_tags = soup.find_all('script', type='application/ld+json')

        # Iterate over script tags and look for required fields in the JSON content
        for script in script_tags:
            try:
                script_content = json.loads(script.string)
                if 'headline' in script_content and 'articleBody' in script_content:
                    headline = script_content['headline']
                    article_body = script_content['articleBody']
                    description = script_content.get('description', 'No description provided')
                    image = script_content.get('image', 'No image provided')
                    return {
                        'title': headline,
                        'posturl': news_details_page_url,
                        'image': image,
                        'highlights': article_body # TODO: Call simplifier and simplify the article body
                    }
            except (json.JSONDecodeError, TypeError) as e:
                continue
        
        return None

def save_news_to_db():
    MAX_NEWS = 5
    news = News(num_news=MAX_NEWS)
    india_today_news = news.fetch_india_today_news()
    indian_express_news = news.fetch_india_express_news()
    logger.info(f"India Today News: {india_today_news}")
    summariser = Summarizer(model_name="gemini")
    total_news = india_today_news + indian_express_news

    for news_item in total_news:
        try:
            if len(news_item['highlights']) > 500:
                news_item['highlights'] = summariser.summarize(news_item['highlights'])
                logger.info(f"Summarized news: {news_item['highlights']}")
                logger.info(f'To avoid bot detection, sleeping for 60 seconds...')
                time.sleep(60)
            logger.info(f"Saving news to database: {news_item}")
            blog = Blog(title=news_item['title'], content=news_item['highlights'], image_url=news_item['image'], news_source=news_item['posturl'])
            blog.save()
        except Exception as e:
            logger.error(f"Error saving news to database: {str(e)}")
            continue

# save_news_to_db()