"""Parser for code files to extract comments."""

import re
from pathlib import Path
from typing import List
from .base import BaseParser, ParsedChunk


class CodeParser(BaseParser):
    """Parser for extracting comments from code files."""

    # Common code file extensions
    CODE_EXTENSIONS = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".jsx": "javascript",
        ".java": "java",
        ".c": "c",
        ".cpp": "cpp",
        ".h": "c",
        ".hpp": "cpp",
        ".go": "go",
        ".rs": "rust",
        ".rb": "ruby",
        ".php": "php",
        ".sh": "shell",
        ".bash": "shell",
    }

    # Comment patterns for different languages
    COMMENT_PATTERNS = {
        "single_line": [
            r"#\s*(TODO|FIXME|BUG|HACK|XXX|NOTE|FEATURE|IDEA)[\s:]*(.+)",  # Python, Ruby, Shell
            r"//\s*(TODO|FIXME|BUG|HACK|XXX|NOTE|FEATURE|IDEA)[\s:]*(.+)",  # JS, Java, C, etc.
        ],
        "any_comment": [
            r"#\s*(.+)",  # Python, Ruby, Shell
            r"//\s*(.+)",  # JS, Java, C, etc.
        ],
    }

    def can_parse(self, file_path: str) -> bool:
        """Check if file is a code file."""
        path = Path(file_path)
        return path.suffix in self.CODE_EXTENSIONS

    def get_source_type(self) -> str:
        """Get source type."""
        return "code"

    def parse(self, file_path: str) -> List[ParsedChunk]:
        """Parse code file and extract relevant comments."""
        path = Path(file_path)
        language = self.CODE_EXTENSIONS.get(path.suffix, "unknown")

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        chunks = []
        for line_num, line in enumerate(lines, start=1):
            # Check for TODO/FIXME/BUG comments first
            for pattern in self.COMMENT_PATTERNS["single_line"]:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    comment_text = line.strip()
                    chunks.append(
                        ParsedChunk(
                            text=comment_text,
                            source_type=self.get_source_type(),
                            source_file=file_path,
                            source_line=line_num,
                            metadata={"language": language, "comment_type": "action"},
                        )
                    )
                    break

        # If no specific action comments found, include all comments
        if not chunks:
            for line_num, line in enumerate(lines, start=1):
                for pattern in self.COMMENT_PATTERNS["any_comment"]:
                    match = re.search(pattern, line)
                    if match:
                        comment_text = line.strip()
                        # Filter out very short or likely non-actionable comments
                        if len(comment_text) > 15:
                            chunks.append(
                                ParsedChunk(
                                    text=comment_text,
                                    source_type=self.get_source_type(),
                                    source_file=file_path,
                                    source_line=line_num,
                                    metadata={"language": language, "comment_type": "general"},
                                )
                            )
                        break

        return chunks
