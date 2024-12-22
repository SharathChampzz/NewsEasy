"""Main module for fetching news from various sources and saving them to the database."""

import logging
import time
from typing import List
from backend.blogs_api.models import Blog
from NewsEasy.scrapper.database import NewsDatabase
from NewsEasy.scrapper.factory import NewsScraperFactory
from NewsEasy.scrapper.text_summarizer import create_summarizer

logger = logging.getLogger(__name__)


def save_news_to_db(
    sources: List[str] = ["india_today", "indian_express"], num_news: int = 5
):
    """Fetch news from the specified sources and save them to the database."""
    db = NewsDatabase()
    seen_news = db.load_seen_news()
    # summarizer = create_summarizer(model_type="gemini")
    summarizer = create_summarizer(model_type="local")

    all_news = []
    for source in sources:
        try:
            scraper = NewsScraperFactory.create_scraper(source, num_news)
            news_items = scraper.fetch_news(seen_news)
            all_news.extend(news_items)
        except Exception as e:
            logger.error("Error fetching news from %s: %s", source, str(e))
            continue

    for item in all_news:
        try:
            highlights = item.highlights
            if len(highlights) > 500:
                highlights = summarizer.summarize(highlights)
                logger.info("Summarized news: %s", highlights)
                time.sleep(60)

            blog = Blog(
                title=item.title,
                content=highlights,
                image_url=item.image_url,
                news_source=item.post_url,
            )
            blog.save()
            db.save_news(item.title, True)

        except Exception as e:
            logger.error("Error saving news to database: %s", str(e))
            db.save_news(item.title, False)
            continue


# if __name__ == "__main__":
#     save_news_to_db()
