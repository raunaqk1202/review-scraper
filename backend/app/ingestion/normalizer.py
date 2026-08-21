import hashlib
from typing import Dict, Any

class Normalizer:
    @staticmethod
    def generate_content_hash(text: str, platform: str, date: str) -> str:
        """Generate a unique hash for a piece of feedback to prevent duplicates."""
        # Simple hash combining text and platform to ensure uniqueness
        unique_string = f"{platform}|{date}|{text}"
        return hashlib.sha256(unique_string.encode('utf-8')).hexdigest()
