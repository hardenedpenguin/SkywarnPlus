"""
Custom exceptions for SkywarnPlus.
"""


class SkywarnPlusError(Exception):
    """Base exception for SkywarnPlus."""
    pass


class ConfigurationError(SkywarnPlusError):
    """Raised when there's an error with configuration."""
    pass


class APIError(SkywarnPlusError):
    """Raised when there's an error with API calls."""
    pass


class AudioProcessingError(SkywarnPlusError):
    """Raised when there's an error with audio processing."""
    pass


class FileIOError(SkywarnPlusError):
    """Raised when there's an error with file I/O operations."""
    pass


class ValidationError(SkywarnPlusError):
    """Raised when data validation fails."""
    pass


class NetworkError(SkywarnPlusError):
    """Raised when there's a network-related error."""
    pass


class TimeoutError(SkywarnPlusError):
    """Raised when an operation times out."""
    pass
