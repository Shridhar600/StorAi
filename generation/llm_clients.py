import requests
import json
import traceback
from abc import ABC, abstractmethod
from datetime import datetime

from config.settings import LLM_API_KEY, LLM_MODEL, LLM_BASE_URL


class LLMError(Exception):
    """Custom exception for LLM-related errors."""
    pass


class TweetGenerationError(Exception):
    """Custom exception for errors during tweet generation."""
    pass

#Abstract base class for LLM clients
class LLMClient(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        """Generates text based on the given prompt."""
        pass

#python inheritance
class OpenRouterClient(LLMClient): #subclass of LLMClient
    """LLM client for interacting with the OpenRouter API."""

    def __init__(self, api_key: str = LLM_API_KEY, model: str = LLM_MODEL, base_url: str = LLM_BASE_URL):
        self.api_key = api_key
        self.model = model
        self.url = f"{base_url}/chat/completions"

    def generate_text(self, prompt: str) -> str:
        """Generates text using the OpenRouter API."""
        print(f"Generating text from LLM with prompt: {prompt}")
        print(f"Model: {self.model}")
        print(f"URL: {self.url}")
        print(f"API Key")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 2.0
        }

        try:
            response = requests.post(
                self.url,
                headers=headers,
                json=data
            )
            response.raise_for_status()

            result = response.json()
            tweet_text = result['choices'][0]['message']['content'].strip().strip('"').strip()

            if len(tweet_text) > 280:
                tweet_text = tweet_text[:277] + "..."

            return tweet_text

        except requests.exceptions.RequestException as e:
            raise LLMError(f"Request to LLM failed: {e}") from e
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            raise LLMError(f"Error parsing LLM response: {e}") from e
        except Exception as e:
            raise LLMError(f"An unexpected error occurred: {e}") from e

class OpenAiClient(LLMClient):
    """LLM client for interacting with the OpenAI API."""
    pass