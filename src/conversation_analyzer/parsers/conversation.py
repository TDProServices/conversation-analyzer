"""Parser for conversation files (Markdown, JSON)."""

import json
from pathlib import Path
from typing import List
from .base import BaseParser, ParsedChunk


class ConversationParser(BaseParser):
    """Parser for conversation files."""

    def can_parse(self, file_path: str) -> bool:
        """Check if file is a conversation file."""
        path = Path(file_path)
        return path.suffix in [".md", ".markdown", ".json"]

    def get_source_type(self) -> str:
        """Get source type."""
        return "conversation"

    def parse(self, file_path: str) -> List[ParsedChunk]:
        """Parse conversation file."""
        path = Path(file_path)

        if path.suffix == ".json":
            return self._parse_json(file_path)
        else:
            return self._parse_markdown(file_path)

    def _parse_markdown(self, file_path: str) -> List[ParsedChunk]:
        """Parse Markdown conversation file."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # For now, treat the entire conversation as one chunk
        # Could be enhanced to split into messages or sections
        return [
            ParsedChunk(
                text=content,
                source_type=self.get_source_type(),
                source_file=file_path,
                metadata={"format": "markdown"},
            )
        ]

    def _parse_json(self, file_path: str) -> List[ParsedChunk]:
        """Parse JSON conversation file."""
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Handle different JSON formats
        if isinstance(data, list):
            # List of messages
            text = self._messages_to_text(data)
        elif isinstance(data, dict):
            if "messages" in data:
                text = self._messages_to_text(data["messages"])
            elif "conversation" in data:
                text = self._messages_to_text(data["conversation"])
            else:
                # Generic dict, convert to text
                text = json.dumps(data, indent=2)
        else:
            text = str(data)

        return [
            ParsedChunk(
                text=text,
                source_type=self.get_source_type(),
                source_file=file_path,
                metadata={"format": "json"},
            )
        ]

    def _messages_to_text(self, messages: list) -> str:
        """Convert list of messages to text."""
        lines = []
        for msg in messages:
            if isinstance(msg, dict):
                role = msg.get("role", msg.get("speaker", "Unknown"))
                content = msg.get("content", msg.get("text", msg.get("message", "")))
                lines.append(f"**{role.title()}:** {content}")
            else:
                lines.append(str(msg))

        return "\n\n".join(lines)
