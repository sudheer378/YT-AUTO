"""YT Auto Helper Functions."""

import re
import time
from datetime import datetime
from typing import Any


def generate_timestamp() -> str:
    """Generate a formatted timestamp string.
    
    Returns:
        Timestamp string in YYYYMMDD_HHMMSS format
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def sanitize_filename(filename: str) -> str:
    """Sanitize a string for use as a filename.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename safe for filesystems
    """
    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', "_", filename)
    # Replace multiple spaces/underscores with single underscore
    sanitized = re.sub(r"[\s_]+", "_", sanitized)
    # Remove leading/trailing underscores
    sanitized = sanitized.strip("_")
    # Limit length
    if len(sanitized) > 100:
        name, ext = sanitized.rsplit(".", 1) if "." in sanitized else (sanitized, "")
        sanitized = name[:95] + ("." + ext if ext else "")
    return sanitized


def calculate_score(
    weights: dict[str, float],
    scores: dict[str, float],
    normalize: bool = True,
) -> float:
    """Calculate weighted score from multiple metrics.
    
    Args:
        weights: Dictionary of metric names to weights
        scores: Dictionary of metric names to scores (0-1)
        normalize: Whether to normalize the result to 0-1
        
    Returns:
        Weighted average score
    """
    total_weight = sum(weights.values())
    if total_weight == 0:
        return 0.0
    
    weighted_sum = 0.0
    for metric, weight in weights.items():
        score = scores.get(metric, 0.0)
        weighted_sum += weight * score
    
    result = weighted_sum / total_weight
    
    if normalize:
        result = max(0.0, min(1.0, result))
    
    return result


def format_duration(seconds: int) -> str:
    """Format duration in seconds to human-readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string (e.g., "10m 30s")
    """
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds}s" if remaining_seconds else f"{minutes}m"
    else:
        hours = seconds // 3600
        remaining_minutes = (seconds % 3600) // 60
        return f"{hours}h {remaining_minutes}m"


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
):
    """Decorator for retrying functions with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay between retries in seconds
        max_delay: Maximum delay between retries in seconds
        
    Returns:
        Decorated function
    """
    def decorator(func):
        import functools
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        delay = min(base_delay * (2 ** attempt), max_delay)
                        time.sleep(delay)
            raise last_exception
        
        return wrapper
    return decorator


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length with suffix.
    
    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to append when truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def safe_get(data: dict | list | None, *keys: Any, default: Any = None) -> Any:
    """Safely get nested dictionary/list values.
    
    Args:
        data: Dictionary or list to traverse
        *keys: Keys/indexes to traverse
        default: Default value if key not found
        
    Returns:
        Value at nested location or default
    """
    if data is None:
        return default
    
    current = data
    for key in keys:
        try:
            if isinstance(current, dict):
                current = current[key]
            elif isinstance(current, list) and isinstance(key, int):
                current = current[key]
            else:
                return default
        except (KeyError, IndexError, TypeError):
            return default
    
    return current
