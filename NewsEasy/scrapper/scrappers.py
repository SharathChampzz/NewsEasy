"""Module containing classes for scraping news from various sources."""

import logging
import json
import time
from typing import List, Optional, Tuple, Set

from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from lxml import html
from NewsEasy.scrapper.models import NewsItem

logger = logging.getLogger(__name__)


class NewsScraper(ABC):
    """Abstract base class for news scrapers."""

    def __init__(self, base_url: str, num_news: int):
        self.base_url = base_url
        self.num_news = num_news

    @abstractmethod
    def fetch_news(self, seen_news: Set[str]) -> List[NewsItem]:
        """Fetch news items from the source."""
        pass

    def _make_request(self, url: str) -> requests.Response:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        return response


class IndiaToday(NewsScraper):
    """Class to scrape news from India Today website."""

    def fetch_news(self, seen_news: Set[str]) -> List[NewsItem]:
        """Fetch news items from India Today website."""
        logger.info("Fetching news from %s...", self.base_url)
        response = self._make_request(self.base_url)

        soup = BeautifulSoup(response.text, "html.parser")
        elements = soup.select(
            ".B1S3_story__card__A_fhi .B1S3_content__thumbnail__wrap__iPgcS .B1S3_story__thumbnail___pFy6 a"
        )

        news_items = []
        count = 0

        for post in elements:
            if count >= self.num_news:
                break

            title = post.get("title")
            if title in seen_news:
                continue

            try:
                post_url = f"{self.base_url}{post.get('href')}"
                image_url = post.find("img").get("src").split("&size=")[0]

                news_details = self._make_request(post_url)
                news_soup = BeautifulSoup(news_details.text, "html.parser")
                news_highlights = news_soup.select(
                    "ul.Story_highlights__list__FRRjs li"
                )
                highlights = "<br>".join(
                    [highlight.get_text() for highlight in news_highlights]
                )

                news_items.append(
                    NewsItem(
                        title=title,
                        post_url=post_url,
                        image_url=image_url,
                        highlights=highlights,
                    )
                )

                count += 1
                logger.info("Sleeping for 60 seconds to avoid detection...")
                time.sleep(60)

            except Exception as e:
                logger.error(f"Error processing news: {title}. Error: {e}")
                raise

        return news_items


class IndianExpress(NewsScraper):
    """Class to scrape news from Indian Express website."""

    def __init__(self, base_url: str, num_news: int):
        super().__init__(base_url, num_news)
        self.xpath_selectors = [
            "//*[@class='other-article ']//*[@class='content-txt']//h3//a",
            "//*[@class='top-news']//h3//a",
        ]

    def fetch_news(self, seen_news: Set[str]) -> List[NewsItem]:
        links_with_titles = self._scrape_links()
        news_items = []
        count = 0

        for title, link in links_with_titles:
            if count >= self.num_news or title in seen_news:
                continue

            try:
                news_details = self._scrape_article(link)
                if news_details:
                    news_items.append(news_details)
                    count += 1
                    logger.info("Sleeping for 60 seconds to avoid detection...")
                    time.sleep(60)

            except Exception as e:
                logger.error(f"Error processing news: {link}. Error: {e}")
                raise

        return news_items

    def _scrape_links(self) -> List[Tuple[str, str]]:
        response = self._make_request(self.base_url)
        tree = html.fromstring(response.content)

        links_with_titles = []
        for xpath in self.xpath_selectors:
            elements = tree.xpath(xpath)
            for element in elements:
                href = element.get("href")
                title = element.text_content().strip()
                if href and title:
                    links_with_titles.append((title, href))

        return links_with_titles

    def _scrape_article(self, url: str) -> Optional[NewsItem]:
        response = self._make_request(url)
        soup = BeautifulSoup(response.text, "html.parser")
        script_tags = soup.find_all("script", type="application/ld+json")

        for script in script_tags:
            try:
                content = json.loads(script.string)
                if "headline" in content and "articleBody" in content:
                    return NewsItem(
                        title=content["headline"],
                        post_url=url,
                        image_url=content.get("image", ""),
                        highlights=content["articleBody"],
                    )
            except (json.JSONDecodeError, TypeError):
                continue

        return None
