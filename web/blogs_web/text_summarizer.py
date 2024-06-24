from transformers import pipeline
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GEN_AI_API_KEY = os.getenv("GEN_AI_API_KEY") # https://aistudio.google.com/app/apikey

class Summarizer:
    def __init__(self, model_name):
        self.model_name = model_name
        self.model = self.initialize_model()

    def initialize_model(self):
        if self.model_name == "local":
            return self.initialize_local_model()
        elif self.model_name == "gemini":
            return self.initialize_gemini_model()
        else:
            raise ValueError("Unsupported model name")

    def initialize_local_model(self):
        print('Local model is initializing...')
        summarizer = pipeline("summarization")
        return summarizer

    def initialize_gemini_model(self):
        print('Gemini model is initializing...')
        # Configure generative AI model
        genai.configure(api_key=GEN_AI_API_KEY)

        GENERATION_CONFIG = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 0,
            "max_output_tokens": 2048,
            "response_mime_type": "text/plain",
        }
        model = genai.GenerativeModel(
            model_name="gemini-1.0-pro-001",
            generation_config=GENERATION_CONFIG,
        )
        chat_session = model.start_chat(history=[])
        return chat_session

    def summarize(self, text, max_length=100, min_length=30):
        if self.model_name == "local":
            return self.summarize_with_local_model(text, max_length, min_length)
        elif self.model_name == "gemini":
            return self.summarize_with_gemini_ai(text, max_length, min_length)

    def summarize_with_local_model(self, text, max_length=100, min_length=30):
        """Summarize text using the local model."""
        print(f'Text to summarize: {text}, max_length={max_length}, min_length={min_length}')
        max_length = 4096  # Adjust this limit as needed (consider model limitations)
        if len(text) > max_length:
            text = text[:max_length]
            print(f"Truncated long text to {max_length} characters.")

        # Recommended summarization parameters
        summary = self.model(text, max_length=75, min_length=min_length)[0]['summary_text']
        print(f'Summary of the text: {summary}')
        return summary

    def summarize_with_gemini_ai(self, text, max_length=100, min_length=30):
        """Summarize text using Gemini AI."""
        prompt = (
            f'Please provide a concise summary of the following text (between {min_length} and {max_length} words): {text}'
        )
        response = self.model.send_message(prompt)
        return response.text

# # Usage example
# summarizer = Summarizer(model_name="local")  # or "gemini"
# text_to_summarize = "Your long news article text here."
# summary = summarizer.summarize(text_to_summarize, max_length=100, min_length=30)
# print("Final Summary:", summary)
