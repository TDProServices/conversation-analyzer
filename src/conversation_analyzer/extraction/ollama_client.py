"""Ollama client for LLM communication."""

import json
import time
from typing import Dict, Any, Optional
import ollama
from ollama import ResponseError

from ..config import OllamaConfig


class OllamaClient:
    """Client for Ollama LLM service."""

    def __init__(self, config: OllamaConfig):
        """Initialize Ollama client."""
        self.config = config
        self.client = ollama.Client(host=config.host)

    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_retries: int = 3,
    ) -> str:
        """Generate response from Ollama."""
        model = model or self.config.extraction_model
        temperature = temperature if temperature is not None else self.config.temperature

        for attempt in range(max_retries):
            try:
                response = self.client.generate(
                    model=model,
                    prompt=prompt,
                    options={
                        "temperature": temperature,
                        "num_predict": self.config.max_tokens,
                    },
                )
                return response["response"]

            except ResponseError as e:
                if attempt == max_retries - 1:
                    raise OllamaConnectionError(f"Failed after {max_retries} attempts: {e}")
                time.sleep(2 ** attempt)  # Exponential backoff

            except Exception as e:
                raise OllamaError(f"Unexpected error: {e}")

    def chat(
        self,
        messages: list,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_retries: int = 3,
    ) -> str:
        """Chat with Ollama model."""
        model = model or self.config.extraction_model
        temperature = temperature if temperature is not None else self.config.temperature

        for attempt in range(max_retries):
            try:
                response = self.client.chat(
                    model=model,
                    messages=messages,
                    options={
                        "temperature": temperature,
                        "num_predict": self.config.max_tokens,
                    },
                )
                return response["message"]["content"]

            except ResponseError as e:
                if attempt == max_retries - 1:
                    raise OllamaConnectionError(f"Failed after {max_retries} attempts: {e}")
                time.sleep(2 ** attempt)

            except Exception as e:
                raise OllamaError(f"Unexpected error: {e}")

    def extract_json(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Generate and parse JSON response."""
        response = self.generate(prompt, model, temperature)
        return self._parse_json_response(response)

    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON from LLM response, handling common issues."""
        # Try direct parsing first
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass

        # Try to extract JSON from markdown code block
        if "```json" in response:
            try:
                json_str = response.split("```json")[1].split("```")[0].strip()
                return json.loads(json_str)
            except (IndexError, json.JSONDecodeError):
                pass

        # Try to extract JSON by finding first { and last }
        try:
            start = response.find("{")
            end = response.rfind("}") + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass

        # If all else fails, raise error
        raise JSONParseError(f"Could not parse JSON from response: {response[:200]}...")

    def test_connection(self) -> bool:
        """Test if Ollama is accessible."""
        try:
            self.client.list()
            return True
        except Exception:
            return False

    def is_model_available(self, model_name: str) -> bool:
        """Check if a model is available locally."""
        try:
            models = self.client.list()
            return any(m["name"].startswith(model_name) for m in models["models"])
        except Exception:
            return False

    def pull_model(self, model_name: str):
        """Pull a model from Ollama registry."""
        try:
            self.client.pull(model_name)
        except Exception as e:
            raise OllamaError(f"Failed to pull model {model_name}: {e}")


class OllamaError(Exception):
    """Base exception for Ollama errors."""

    pass


class OllamaConnectionError(OllamaError):
    """Ollama connection error."""

    pass


class JSONParseError(OllamaError):
    """JSON parsing error from LLM response."""

    pass
