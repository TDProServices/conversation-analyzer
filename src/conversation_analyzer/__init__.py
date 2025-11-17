"""
Conversation Analyzer - Local LLM-powered conversation analysis

This package analyzes Claude Code conversations and project files to automatically
extract missed TODOs, bugs, feature requests, and potential automation opportunities.

Key Features:
- 100% local/offline using Ollama (privacy-first)
- Extracts explicit and implicit action items
- Deduplicates findings across conversations
- Generates prioritized reports
- Confidence scoring for each finding

Author: Tanya Davis / TD Professional Services LLC
License: MIT
"""

__version__ = "0.1.0"
__author__ = "Tanya Davis"
__email__ = "[email protected]"

# Export main components (to be implemented)
# from .parser import ConversationParser
# from .analyzer import ConversationAnalyzer
# from .extractor import TODOExtractor
# from .reporter import ReportGenerator

__all__ = [
    "__version__",
    "__author__",
    # "ConversationParser",
    # "ConversationAnalyzer",
    # "TODOExtractor",
    # "ReportGenerator",
]
