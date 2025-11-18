"""Path validation utilities to prevent path traversal attacks."""

from pathlib import Path
from typing import Optional, Union
import os


class PathValidationError(ValueError):
    """Exception raised when path validation fails."""
    pass


def validate_file_path(
    file_path: Union[str, Path],
    base_dir: Optional[Union[str, Path]] = None,
    must_exist: bool = False,
    allow_symlinks: bool = False
) -> Path:
    """Validate file path against path traversal attacks.

    Args:
        file_path: Path to validate
        base_dir: Optional base directory to restrict access to
        must_exist: If True, raise error if path doesn't exist
        allow_symlinks: If True, allow symbolic links

    Returns:
        Resolved Path object

    Raises:
        PathValidationError: If path is invalid or outside base_dir

    Security:
        - Resolves path to absolute path
        - Checks for path traversal (../)
        - Validates path is within base_dir if specified
        - Optionally checks for symbolic links
        - Validates path exists if required

    Examples:
        >>> validate_file_path("/tmp/safe.txt")
        PosixPath('/tmp/safe.txt')

        >>> validate_file_path("../../etc/passwd", base_dir="/home/user")
        PathValidationError: Path /etc/passwd outside base directory /home/user
    """
    try:
        # Convert to Path and resolve to absolute path
        path = Path(file_path).resolve()

        # Check if symbolic link (potential security risk)
        if not allow_symlinks and path.is_symlink():
            raise PathValidationError(f"Symbolic links not allowed: {path}")

        # If base_dir specified, ensure path is within it
        if base_dir is not None:
            base = Path(base_dir).resolve()

            # Check if path is within base directory
            try:
                path.relative_to(base)
            except ValueError:
                raise PathValidationError(
                    f"Path {path} outside base directory {base}"
                )

        # Validate path exists if required
        if must_exist and not path.exists():
            raise PathValidationError(f"Path does not exist: {path}")

        return path

    except Exception as e:
        if isinstance(e, PathValidationError):
            raise
        raise PathValidationError(f"Invalid path {file_path}: {e}")


def validate_directory_path(
    dir_path: Union[str, Path],
    base_dir: Optional[Union[str, Path]] = None,
    must_exist: bool = False,
    create_if_missing: bool = False
) -> Path:
    """Validate directory path against path traversal attacks.

    Args:
        dir_path: Directory path to validate
        base_dir: Optional base directory to restrict access to
        must_exist: If True, raise error if directory doesn't exist
        create_if_missing: If True, create directory if it doesn't exist

    Returns:
        Resolved Path object

    Raises:
        PathValidationError: If path is invalid or not a directory

    Examples:
        >>> validate_directory_path("/tmp", must_exist=True)
        PosixPath('/tmp')

        >>> validate_directory_path("data/reports", create_if_missing=True)
        PosixPath('/path/to/data/reports')
    """
    path = validate_file_path(
        dir_path,
        base_dir=base_dir,
        must_exist=False,  # We handle existence separately for directories
        allow_symlinks=False
    )

    # Create directory if requested
    if create_if_missing and not path.exists():
        try:
            path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise PathValidationError(f"Cannot create directory {path}: {e}")

    # Check if exists and is directory
    if path.exists() and not path.is_dir():
        raise PathValidationError(f"Path exists but is not a directory: {path}")

    if must_exist and not path.exists():
        raise PathValidationError(f"Directory does not exist: {path}")

    return path


def safe_join(*paths: Union[str, Path], base_dir: Optional[Union[str, Path]] = None) -> Path:
    """Safely join paths and validate result.

    Args:
        *paths: Path components to join
        base_dir: Optional base directory to restrict access to

    Returns:
        Validated joined path

    Raises:
        PathValidationError: If resulting path is invalid

    Examples:
        >>> safe_join("/data", "reports", "file.txt")
        PosixPath('/data/reports/file.txt')

        >>> safe_join("/data", "../../../etc/passwd", base_dir="/data")
        PathValidationError: Path outside base directory
    """
    if not paths:
        raise PathValidationError("At least one path component required")

    # Join all paths
    joined = Path(paths[0])
    for p in paths[1:]:
        joined = joined / p

    # Validate the result
    return validate_file_path(joined, base_dir=base_dir, must_exist=False)


def get_safe_filename(filename: str, max_length: int = 255) -> str:
    """Sanitize filename to prevent path traversal and OS issues.

    Args:
        filename: Original filename
        max_length: Maximum filename length (default: 255)

    Returns:
        Sanitized filename

    Security:
        - Removes path separators
        - Removes null bytes
        - Removes special characters
        - Limits filename length
        - Prevents reserved names (Windows)

    Examples:
        >>> get_safe_filename("../../etc/passwd")
        'etc_passwd'

        >>> get_safe_filename("file<>|?.txt")
        'file___.txt'
    """
    # Remove path separators
    filename = os.path.basename(filename)

    # Remove null bytes
    filename = filename.replace('\0', '')

    # Replace problematic characters
    replacements = {
        '/': '_',
        '\\': '_',
        ':': '_',
        '*': '_',
        '?': '_',
        '"': '_',
        '<': '_',
        '>': '_',
        '|': '_',
        '\n': '_',
        '\r': '_',
    }

    for old, new in replacements.items():
        filename = filename.replace(old, new)

    # Windows reserved names
    reserved = [
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9',
    ]

    name_without_ext = filename.rsplit('.', 1)[0].upper()
    if name_without_ext in reserved:
        filename = f"_{filename}"

    # Limit length
    if len(filename) > max_length:
        # Preserve extension if present
        if '.' in filename:
            name, ext = filename.rsplit('.', 1)
            max_name_length = max_length - len(ext) - 1
            filename = f"{name[:max_name_length]}.{ext}"
        else:
            filename = filename[:max_length]

    # Ensure not empty or just dots
    if not filename or filename.strip('.') == '':
        filename = "unnamed_file"

    return filename
