import asyncio
from apify_client import ApifyClient
from typing import List, Dict, Any
from datetime import datetime
from app.ingestion.base_adapter import SourceAdapter
from app.ingestion.normalizer import Normalizer
from app.models.enums import SourcePlatform

class WebReviewsAdapter(SourceAdapter):
    def __init__(self, queries: List[str] = None):
        if not queries:
            self.queries = [
                "myntra wishlist bug site:mouthshut.com", 
                "myntra cart issue site:trustpilot.com"
            ]
        else:
            self.queries = queries
        import os
        self.token = os.environ.get("APIFY_API_TOKEN", "")
        self.client = ApifyClient(self.token)

    @property
    def platform_name(self) -> str:
        return SourcePlatform.PRODUCT_REVIEWS.value

    async def fetch(self, limit: int = 20, **kwargs) -> List[Dict[str, Any]]:
        return await asyncio.to_thread(self._sync_fetch, limit)

    def _sync_fetch(self, limit: int) -> List[Dict[str, Any]]:
        run_input = {
            "queries": "\n".join(self.queries),
            "resultsPerPage": limit,
            "maxPagesPerQuery": 1,
        }
        try:
            print(f"[{self.platform_name}] Starting Apify Google Search scraper for web reviews (this takes ~30 seconds)...")
            run = self.client.actor("apify/google-search-scraper").call(run_input=run_input)
            
            raw_data = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                organic = item.get("organicResults", [])
                raw_data.extend(organic)
            return raw_data
        except Exception as e:
            print(f"[{self.platform_name}] Apify fetch error: {e}")
            return []

    def normalize(self, raw_data: List[Dict[str, Any]]) -> List[dict]:
        normalized = []
        for item in raw_data:
            title = item.get("title", "")
            description = item.get("description", "")
            
            text = f"{title}\n\n{description}".strip()
            if not text:
                continue
                
            normalized.append({
                "original_text": text,
                "source_platform": self.platform_name,
                "source_date": datetime.utcnow(),
                "source_url": item.get("url", ""),
                "thread_id": "",
                "author_id_anonymized": Normalizer.generate_content_hash(item.get("url", "anonymous"), "author", ""),
                "content_hash": Normalizer.generate_content_hash(text, self.platform_name, "now"),
            })
        return normalized
