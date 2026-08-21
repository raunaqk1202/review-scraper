import asyncio
from apify_client import ApifyClient
from typing import List, Dict, Any
from datetime import datetime
from app.ingestion.base_adapter import SourceAdapter
from app.ingestion.normalizer import Normalizer
from app.models.enums import SourcePlatform

class YouTubeAdapter(SourceAdapter):
    def __init__(self, video_urls: List[str] = None):
        if not video_urls:
            # Huge Myntra Haul videos to get relevant shopping comments
            self.video_urls = [
                "https://www.youtube.com/watch?v=FlsCjmMhFmw",
                "https://www.youtube.com/watch?v=jNQXAC9IVRw"
            ]
        else:
            self.video_urls = video_urls
        import os
        self.token = os.environ.get("APIFY_API_TOKEN", "")
        self.client = ApifyClient(self.token)

    @property
    def platform_name(self) -> str:
        return SourcePlatform.YOUTUBE.value

    async def fetch(self, limit: int = 100, **kwargs) -> List[Dict[str, Any]]:
        return await asyncio.to_thread(self._sync_fetch, limit)

    def _sync_fetch(self, limit: int) -> List[Dict[str, Any]]:
        run_input = {
            "startUrls": [{"url": url} for url in self.video_urls],
            "maxComments": limit,
        }
        try:
            print(f"[{self.platform_name}] Starting Apify YouTube Comments scraper (this takes ~30 seconds)...")
            run = self.client.actor("streamers/youtube-comments-scraper").call(run_input=run_input)
            
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
            text = item.get("text", "").strip()
            if not text:
                continue
                
            date_str = item.get("publishedAt", "")
            date_obj = None
            if date_str:
                try:
                    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                except ValueError:
                    date_obj = datetime.utcnow()
            else:
                date_obj = datetime.utcnow()
                    
            normalized.append({
                "original_text": text,
                "source_platform": self.platform_name,
                "source_date": date_obj,
                "source_url": item.get("videoUrl", ""),
                "thread_id": item.get("videoId", ""),
                "author_id_anonymized": Normalizer.generate_content_hash(item.get("authorName", "anonymous"), "author", ""),
                "content_hash": Normalizer.generate_content_hash(text, self.platform_name, str(date_str)),
            })
        return normalized
