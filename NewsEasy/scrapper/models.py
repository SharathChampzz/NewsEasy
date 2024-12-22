"""Module to define data classes for news items."""

from dataclasses import dataclass


@dataclass
class NewsItem:
    """Data class to store news item details."""

    title: str
    post_url: str
    image_url: str
    highlights: str
