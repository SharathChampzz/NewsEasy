"""Module for text summarization using various AI models.

This module provides a flexible interface for summarizing text using either
local transformer models or the Gemini AI API.
"""

from typing import Optional, Any
from dataclasses import dataclass
import os
from enum import Enum, auto

from transformers import pipeline
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ModelType(Enum):
    """Supported model types for text summarization."""

    LOCAL = auto()
    GEMINI = auto()


@dataclass
class GenerationConfig:
    """Configuration settings for text generation."""

    temperature: float = 0.9
    top_p: float = 1.0
    top_k: int = 0
    max_output_tokens: int = 2048
    response_mime_type: str = "text/plain"


class SummarizerError(Exception):
    """Base exception class for Summarizer errors."""


class ModelInitializationError(SummarizerError):
    """Raised when model initialization fails."""


class TextTooLongError(SummarizerError):
    """Raised when input text exceeds maximum length."""


class Summarizer:
    """Text summarization class supporting multiple AI models."""

    MAX_TEXT_LENGTH: int = 4096
    DEFAULT_MIN_LENGTH: int = 30
    DEFAULT_MAX_LENGTH: int = 100

    def __init__(self, model_type: str) -> None:
        """Initialize the summarization model.

        Args:
            model_type: Type of model to use ("local" or "gemini")

        Raises:
            ModelInitializationError: If model initialization fails
            ValueError: If unsupported model type is specified
        """
        try:
            self.model_type = ModelType[model_type.upper()]
            self.model = self._initialize_model()
        except KeyError as exc:
            raise ValueError(
                f"Unsupported model type: {model_type}. Use 'local' or 'gemini'."
            ) from exc
        except Exception as exc:
            raise ModelInitializationError(
                f"Failed to initialize {model_type} model: {str(exc)}"
            ) from exc

    def _initialize_model(self) -> Any:
        """Initialize the appropriate summarization model.

        Returns:
            Initialized model instance

        Raises:
            ModelInitializationError: If model initialization fails
        """
        if self.model_type == ModelType.LOCAL:
            return self._initialize_local_model()
        return self._initialize_gemini_model()

    def _initialize_local_model(self) -> Any:
        """Initialize the local transformer-based summarization model."""
        print("Initializing local model...")
        return pipeline("summarization")

    def _initialize_gemini_model(self) -> Any:
        """Initialize the Gemini AI summarization model."""
        print("Initializing Gemini model...")
        api_key = os.getenv("GEN_AI_API_KEY")
        if not api_key:
            raise ModelInitializationError(
                "Gemini API key not found in environment variables"
            )

        genai.configure(api_key=api_key)
        config = GenerationConfig()
        model = genai.GenerativeModel(
            model_name="gemini-1.0-pro-001",
            generation_config=config.__dict__,
        )
        return model.start_chat(history=[])

    def _validate_text_length(self, text: str) -> None:
        """Validate that text length is within acceptable limits.

        Args:
            text: Input text to validate

        Raises:
            TextTooLongError: If text exceeds maximum length
        """
        if len(text) > self.MAX_TEXT_LENGTH:
            raise TextTooLongError(
                f"Input text length ({len(text)}) exceeds maximum allowed length "
                f"({self.MAX_TEXT_LENGTH})"
            )

    def summarize(
        self,
        text: str,
        max_length: Optional[int] = None,
        min_length: Optional[int] = None,
    ) -> str:
        """Summarize the given text using the initialized model.

        Args:
            text: Text to summarize
            max_length: Maximum length of the summary in words
            min_length: Minimum length of the summary in words

        Returns:
            Summarized text

        Raises:
            TextTooLongError: If input text is too long
            SummarizerError: If summarization fails
        """
        self._validate_text_length(text)

        max_length = max_length or self.DEFAULT_MAX_LENGTH
        min_length = min_length or self.DEFAULT_MIN_LENGTH

        if self.model_type == ModelType.LOCAL:
            return self._summarize_with_local_model(text, max_length, min_length)
        return self._summarize_with_gemini_ai(text, max_length, min_length)

    def _summarize_with_local_model(
        self, text: str, max_length: int, min_length: int
    ) -> str:
        """Summarize text using the local transformer model."""
        try:
            result = self.model(text, max_length=max_length, min_length=min_length)
            return result[0]["summary_text"]
        except Exception as e:
            raise SummarizerError(f"Local model summarization failed: {str(e)}") from e

    def _summarize_with_gemini_ai(
        self, text: str, max_length: int, min_length: int
    ) -> str:
        """Summarize text using Gemini AI."""
        try:
            prompt = (
                f"Please provide a concise summary of the following text "
                f"(between {min_length} and {max_length} words): {text}"
            )
            response = self.model.send_message(prompt)
            return response.text
        except Exception as e:
            raise SummarizerError(f"Gemini AI summarization failed: {str(e)}") from e


def create_summarizer(model_type: str) -> Summarizer:
    """Factory function to create a Summarizer instance.

    Args:
        model_type: Type of model to use ("local" or "gemini")

    Returns:
        Initialized Summarizer instance
    """
    return Summarizer(model_type)


# # Usage Example:

# try:
#     # Create a summarizer instance
#     summarizer = create_summarizer("local")  # or "gemini"

#     # Summarize text
#     text = "Your long article text here..."
#     summary = summarizer.summarize(
#         text, max_length=100, min_length=30  # optional  # optional
#     )
#     print(f"Summary: {summary}")

# except SummarizerError as e:
#     print(f"Summarization failed: {e}")
