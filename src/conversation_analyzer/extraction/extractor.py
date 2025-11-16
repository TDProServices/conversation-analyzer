"""Main extraction orchestrator."""

from typing import List, Optional
from pydantic import ValidationError

from ..models import ExtractedItem, ExtractionResult, Item
from ..config import OllamaConfig, ExtractionConfig
from .ollama_client import OllamaClient, JSONParseError
from .prompts import build_extraction_prompt, build_code_extraction_prompt
from ..parsers.base import ParsedChunk


class Extractor:
    """Orchestrates LLM-based extraction of items."""

    def __init__(self, ollama_config: OllamaConfig, extraction_config: ExtractionConfig):
        """Initialize extractor."""
        self.ollama = OllamaClient(ollama_config)
        self.config = extraction_config

    def extract_from_chunk(self, chunk: ParsedChunk) -> ExtractionResult:
        """Extract items from a parsed chunk."""
        # Build appropriate prompt
        if chunk.source_type == "code":
            prompt = build_code_extraction_prompt(chunk.text, chunk.source_file)
        else:
            prompt = build_extraction_prompt(chunk.text)

        try:
            # Get JSON response from LLM
            response_json = self.ollama.extract_json(prompt)

            # Validate and parse with Pydantic
            result = ExtractionResult(**response_json)

            # Filter by confidence threshold
            filtered_items = [
                item for item in result.items
                if item.confidence >= self.config.confidence_threshold
            ]

            return ExtractionResult(items=filtered_items)

        except JSONParseError as e:
            # Log error and return empty result
            print(f"JSON parse error for {chunk.source_file}: {e}")
            return ExtractionResult(items=[])

        except ValidationError as e:
            # Log validation error and return empty result
            print(f"Validation error for {chunk.source_file}: {e}")
            return ExtractionResult(items=[])

        except Exception as e:
            # Log unexpected error and return empty result
            print(f"Unexpected error for {chunk.source_file}: {e}")
            return ExtractionResult(items=[])

    def extract_from_chunks(self, chunks: List[ParsedChunk]) -> List[Item]:
        """Extract from multiple chunks and convert to Item objects."""
        all_items = []

        for chunk in chunks:
            result = self.extract_from_chunk(chunk)

            for extracted_item in result.items:
                # Convert ExtractedItem to Item with source info
                item = Item(
                    type=extracted_item.type,
                    description=extracted_item.description,
                    priority=extracted_item.priority,
                    priority_score=self._priority_to_score(extracted_item.priority),
                    source_context=extracted_item.source_context,
                    confidence=extracted_item.confidence,
                    source_type=chunk.source_type,
                    source_file=chunk.source_file,
                    source_line=chunk.source_line,
                    metadata=chunk.metadata,
                )
                all_items.append(item)

        return all_items

    def _priority_to_score(self, priority: str) -> float:
        """Convert priority string to numeric score."""
        priority_map = {
            "high": 0.8,
            "medium": 0.5,
            "low": 0.2,
        }
        return priority_map.get(priority, 0.5)

    def test_connection(self) -> bool:
        """Test if Ollama is accessible."""
        return self.ollama.test_connection()

    def ensure_model_available(self, model_name: Optional[str] = None) -> bool:
        """Ensure the extraction model is available."""
        model = model_name or self.ollama.config.extraction_model
        if not self.ollama.is_model_available(model):
            print(f"Model {model} not found. Pulling...")
            self.ollama.pull_model(model)
            return True
        return True
