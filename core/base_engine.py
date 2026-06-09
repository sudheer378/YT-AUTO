"""YT Auto Base Engine."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging

from utils.logger import get_logger


logger = get_logger(__name__)


class BaseEngine(ABC):
    """Abstract base class for all engines."""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"yt_auto.{name}")
    
    @abstractmethod
    async def process(self, *args, **kwargs) -> Any:
        """Process input and return result.
        
        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Processing result
        """
        pass
    
    def validate_input(self, data: Any) -> bool:
        """Validate input data.
        
        Args:
            data: Input data to validate
            
        Returns:
            True if valid, False otherwise
        """
        return data is not None
    
    def handle_error(self, error: Exception, context: Optional[Dict] = None) -> Dict:
        """Handle errors gracefully.
        
        Args:
            error: Exception that occurred
            context: Optional context information
            
        Returns:
            Error response dictionary
        """
        self.logger.error(f"Error in {self.name}: {error}", exc_info=True)
        return {
            "success": False,
            "error": str(error),
            "context": context or {},
        }
