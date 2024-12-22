"""Database module to store seen and failed news."""

import contextlib
import sqlite3
import logging
from typing import Set

logger = logging.getLogger(__name__)


class NewsDatabase:
    """SQLite database to store seen and failed news."""

    def __init__(self, db_path: str = "news_db.sqlite"):
        """Initialize the SQLite database to store seen and failed news"""
        self.db_path = db_path
        self.conn = self._init_connection()

    def _init_connection(self) -> sqlite3.Connection:
        """Initialize the SQLite database to store seen and failed news."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY,
                title TEXT UNIQUE,
                status BOOLEAN
            )
        """
        )
        conn.commit()
        return conn

    def load_seen_news(self) -> Set[str]:
        """Load previously seen news titles from the local database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT title FROM news WHERE status = 1")
        return {row[0] for row in cursor.fetchall()}

    def save_news(self, title: str, status: bool) -> None:
        """Save news to the local database."""
        with contextlib.suppress(sqlite3.IntegrityError):
            cursor = self.conn.cursor()
            logger.info("Saving news to local database: {title}, status={status}")
            cursor.execute(
                "INSERT INTO news (title, status) VALUES (?, ?)", (title, status)
            )
            self.conn.commit()
