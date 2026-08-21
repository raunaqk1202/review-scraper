import asyncio
# pyrefly: ignore [missing-import]
from apify_client import ApifyClient
from typing import List, Dict, Any
from datetime import datetime
from app.ingestion.base_adapter import SourceAdapter
from app.ingestion.normalizer import Normalizer
from app.models.enums import SourcePlatform

class RedditAdapter(SourceAdapter):
    def __init__(self, queries: List[str] = None):
        if not queries:
            self.queries = ["myntra"]
        else:
            self.queries = queries
        import os
        self.token = os.environ.get("APIFY_API_TOKEN", "")
        self.client = ApifyClient(self.token)

    @property
    def platform_name(self) -> str:
        return SourcePlatform.REDDIT.value

    async def fetch(self, limit: int = 50, **kwargs) -> List[Dict[str, Any]]:
        # Run synchronous Apify client in a thread to not block the event loop
        return await asyncio.to_thread(self._sync_fetch, limit)

    def _sync_fetch(self, limit: int) -> List[Dict[str, Any]]:
        run_input = {
            "searches": self.queries,
            "type": "post",
            "sort": "new",
            "maxItems": limit,
        }
        try:
            print(f"[{self.platform_name}] Starting Apify actor (this may take 30-60 seconds to bypass blocks)...")
            run = self.client.actor("trudax/reddit-scraper-lite").call(run_input=run_input)
            
            raw_data = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                raw_data.append(item)
            return raw_data
        except Exception as e:
            print(f"[{self.platform_name}] Apify fetch error: {e}")
            return []

    def normalize(self, raw_data: List[Dict[str, Any]]) -> List[dict]:
        normalized = []
        for item in raw_data:
            title = item.get("title", "")
            body = item.get("text", "")
            
            text = f"{title}\n\n{body}".strip()
            if not text:
                continue
                
            date_str = item.get("createdAt", "")
            date_obj = None
            if date_str:
                try:
                    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                except ValueError:
                    date_obj = datetime.utcnow()
                    
            normalized.append({
                "original_text": text,
                "source_platform": self.platform_name,
                "source_date": date_obj,
                "source_url": item.get("url", ""),
                "thread_id": item.get("id", ""),
                "author_id_anonymized": Normalizer.generate_content_hash(item.get("author", "anonymous"), "author", ""),
                "content_hash": Normalizer.generate_content_hash(text, self.platform_name, str(date_str)),
            })
        return normalized
