"""Conversation Analyzer - Local LLM-powered conversation and code analysis."""

__version__ = "0.1.0"
__author__ = "Tanya Davis / TD Professional Services LLC"

from .models import (
    Item,
    ExtractionResult,
    ExtractedItem,
    Relationship,
    Source,
    ExtractionRun,
    AnalysisResult,
    DuplicateGroup,
)
from .config import Config
from .database import Database
from .analyzer import ConversationAnalyzer

__all__ = [
    # Models
    "Item",
    "ExtractionResult",
    "ExtractedItem",
    "Relationship",
    "Source",
    "ExtractionRun",
    "AnalysisResult",
    "DuplicateGroup",
    # Core classes
    "Config",
    "Database",
    "ConversationAnalyzer",
    # Metadata
    "__version__",
    "__author__",
]
