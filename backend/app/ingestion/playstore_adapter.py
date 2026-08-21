from typing import List, Dict, Any
from datetime import datetime
# pyrefly: ignore [missing-import]
from google_play_scraper import Sort, reviews
from app.ingestion.base_adapter import SourceAdapter
from app.ingestion.normalizer import Normalizer
from app.models.enums import SourcePlatform

class PlayStoreAdapter(SourceAdapter):
    def __init__(self, app_id: str = "com.myntra.android", lang: str = "en", country: str = "in"):
        self.app_id = app_id
        self.lang = lang
        self.country = country

    @property
    def platform_name(self) -> str:
        return SourcePlatform.PLAY_STORE.value

    async def fetch(self, limit: int = 100, **kwargs) -> List[Dict[str, Any]]:
        result, _ = reviews(
            self.app_id,
            lang=self.lang,
            country=self.country,
            sort=Sort.NEWEST,
            count=limit
        )
        return result

    def normalize(self, raw_data: List[Dict[str, Any]]) -> List[dict]:
        normalized = []
        for item in raw_data:
            text = item.get("content", "").strip()
            if not text:
                continue
                
            date_obj = item.get("at")
            date_str = date_obj.isoformat() if isinstance(date_obj, datetime) else str(date_obj)
            
            normalized.append({
                "original_text": text,
                "source_platform": self.platform_name,
                "source_date": date_obj if isinstance(date_obj, datetime) else None,
                "author_id_anonymized": Normalizer.generate_content_hash(item.get("userName", "anonymous"), "author", ""),
                "content_hash": Normalizer.generate_content_hash(text, self.platform_name, date_str),
            })
        return normalized
