# web/blogs_web/tasks.py
import logging
from celery import shared_task
from web.blogs_web.utils import save_news_to_db

logger = logging.getLogger('scheduler')

@shared_task
def scrape_and_save():
    logger.info("Scraping and saving data...")
    try:
        save_news_to_db()
    except Exception as e:
        logger.error(f"Error scraping and saving data: {str(e)}")
        return 1
    logger.info("Data scraping and saving completed successfully.")
    return 0
