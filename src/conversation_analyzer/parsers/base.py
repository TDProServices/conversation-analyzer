"""Base parser interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ParsedChunk:
    """A chunk of parsed text ready for extraction."""

    text: str
    source_type: str  # conversation, code, document, git
    source_file: str
    source_line: Optional[int] = None
    metadata: dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BaseParser(ABC):
    """Base parser interface for different source types."""

    @abstractmethod
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle the given file."""
        pass

    @abstractmethod
    def parse(self, file_path: str) -> List[ParsedChunk]:
        """Parse file and return chunks of text."""
        pass

    @abstractmethod
    def get_source_type(self) -> str:
        """Get the source type this parser handles."""
        pass
