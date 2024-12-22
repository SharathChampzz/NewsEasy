"""Factory class to create news scrapper objects based on the source."""

from NewsEasy.scrapper.scrappers import NewsScraper, IndiaToday, IndianExpress


class NewsScraperFactory:
    """Factory class to create news scrapper objects based on the source."""

    @staticmethod
    def create_scraper(source: str, num_news: int) -> NewsScraper:
        """Create a news scrapper object based on the source."""
        if source == "india_today":
            return IndiaToday("https://www.indiatoday.in", num_news)
        elif source == "indian_express":
            return IndianExpress("https://indianexpress.com/", num_news)
        else:
            raise ValueError(f"Unknown news source: {source}")
