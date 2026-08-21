from abc import ABC, abstractmethod
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
import logging

class PipelineStage(ABC):
    """Abstract base class for all pipeline stages."""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        
    @property
    @abstractmethod
    def stage_name(self) -> str:
        pass
        
    @property
    @abstractmethod
    def stage_number(self) -> int:
        pass
        
    @abstractmethod
    async def process(self, db: AsyncSession, **kwargs) -> Dict[str, Any]:
        """
        Execute the stage logic.
        Returns a dictionary with metrics/results.
        """
        pass
