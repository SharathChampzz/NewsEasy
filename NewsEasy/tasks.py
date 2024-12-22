"""Celery tasks for scraping news and saving them to the database."""
import logging
from celery import shared_task
from web.blogs_web.utils import save_news_to_db

logger = logging.getLogger(__name__)

@shared_task
def scrape_and_save():
    """Scrape news from various sources and save them to the database."""
    logger.info("Scraping and saving data...")
    try:
        save_news_to_db()
    except Exception as e:
        logger.error("Error scraping and saving data: %s", str(e))
        return 1
    logger.info("Data scraping and saving completed successfully.")
    return 0
