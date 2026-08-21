from abc import ABC, abstractmethod
from typing import List, Dict, Any

class SourceAdapter(ABC):
    """Abstract base class for all data ingestion adapters."""
    
    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Name of the platform (e.g., PLAY_STORE, APP_STORE)"""
        pass

    @abstractmethod
    async def fetch(self, limit: int = 100, **kwargs) -> List[Dict[str, Any]]:
        """Fetch raw data from the source."""
        pass

    @abstractmethod
    def normalize(self, raw_data: List[Dict[str, Any]]) -> List[dict]:
        """Normalize raw data into the unified FeedbackItem schema."""
        pass
