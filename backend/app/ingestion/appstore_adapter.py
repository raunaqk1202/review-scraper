from typing import List, Dict, Any
from datetime import datetime
import logging
from app.ingestion.base_adapter import SourceAdapter
from app.ingestion.normalizer import Normalizer
from app.models.enums import SourcePlatform

logger = logging.getLogger(__name__)

class AppStoreAdapter(SourceAdapter):
    def __init__(self, app_name: str = "myntra-fashion-shopping-app", app_id: int = 907394059, country: str = "in"):
        self.app_name = app_name
        self.app_id = app_id
        self.country = country

    @property
    def platform_name(self) -> str:
        return SourcePlatform.APP_STORE.value

    async def fetch(self, limit: int = 100, **kwargs) -> List[Dict[str, Any]]:
        try:
            from app_store_scraper import AppStore
        except ImportError:
            logger.error("app-store-scraper is not installed. Install it with: pip install app-store-scraper==0.3.5 --no-deps")
            raise RuntimeError("app-store-scraper package is not installed")
        myntra = AppStore(country=self.country, app_name=self.app_name, app_id=self.app_id)
        myntra.review(how_many=limit)
        return myntra.reviews

    def normalize(self, raw_data: List[Dict[str, Any]]) -> List[dict]:
        normalized = []
        for item in raw_data:
            title = item.get("title", "")
            review = item.get("review", "")
            text = f"{title}. {review}".strip() if title else review.strip()
            
            if not text:
                continue
                
            date_obj = item.get("date")
            date_str = date_obj.isoformat() if isinstance(date_obj, datetime) else str(date_obj)
            
            normalized.append({
                "original_text": text,
                "source_platform": self.platform_name,
                "source_date": date_obj if isinstance(date_obj, datetime) else None,
                "author_id_anonymized": Normalizer.generate_content_hash(item.get("userName", "anonymous"), "author", ""),
                "content_hash": Normalizer.generate_content_hash(text, self.platform_name, date_str),
            })
        return normalized

