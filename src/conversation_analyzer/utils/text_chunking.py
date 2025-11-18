"""Text chunking utilities for handling context window limits."""

from typing import List


def chunk_text(text: str, max_tokens: int = 1800, overlap: int = 100) -> List[str]:
    """Chunk text into smaller pieces with overlap.

    Args:
        text: Text to chunk
        max_tokens: Maximum tokens per chunk (approximate as chars/4)
        overlap: Number of characters to overlap between chunks

    Returns:
        List of text chunks
    """
    # Approximate: 1 token ≈ 4 characters
    max_chars = max_tokens * 4

    if len(text) <= max_chars:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + max_chars

        # Try to break at sentence boundary
        if end < len(text):
            # Look for sentence endings near the boundary
            for i in range(end, max(start, end - 200), -1):
                if text[i] in ".!?\n":
                    end = i + 1
                    break

        chunks.append(text[start:end])

        # Move start forward, accounting for overlap
        start = end - overlap

        if start >= len(text):
            break

    return chunks


def estimate_tokens(text: str) -> int:
    """Estimate number of tokens in text.

    Uses simple heuristic: 1 token ≈ 4 characters

    Args:
        text: Text to estimate

    Returns:
        Estimated token count
    """
    return len(text) // 4


def truncate_text(text: str, max_tokens: int = 2000) -> str:
    """Truncate text to max tokens.

    Args:
        text: Text to truncate
        max_tokens: Maximum tokens

    Returns:
        Truncated text
    """
    max_chars = max_tokens * 4
    if len(text) <= max_chars:
        return text

    # Truncate and add ellipsis
    return text[:max_chars - 3] + "..."
