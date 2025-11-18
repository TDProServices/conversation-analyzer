"""File hashing utilities."""

import hashlib
from pathlib import Path


def calculate_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """Calculate hash of a file.

    Args:
        file_path: Path to file
        algorithm: Hash algorithm (sha256, md5, sha1)

    Returns:
        Hex digest of file hash
    """
    hash_func = getattr(hashlib, algorithm)()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)

    return hash_func.hexdigest()


def calculate_string_hash(text: str, algorithm: str = "sha256") -> str:
    """Calculate hash of a string.

    Args:
        text: Text to hash
        algorithm: Hash algorithm

    Returns:
        Hex digest of hash
    """
    hash_func = getattr(hashlib, algorithm)()
    hash_func.update(text.encode("utf-8"))
    return hash_func.hexdigest()


def files_are_identical(file1: str, file2: str) -> bool:
    """Check if two files have identical content via hash.

    Args:
        file1: First file path
        file2: Second file path

    Returns:
        True if files are identical
    """
    return calculate_file_hash(file1) == calculate_file_hash(file2)
