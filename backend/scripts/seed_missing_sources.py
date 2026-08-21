import asyncio
import os
import sys
from datetime import datetime
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import AsyncSessionLocal
from app.models.feedback import DataSource, FeedbackItem
from app.ingestion.normalizer import Normalizer
from sqlalchemy.future import select

MOCK_DATA = {
    "APP_STORE": [
        "The size charts are incredibly confusing for shoes.",
        "Cart keeps crashing when I try to add multiple items from wishlist.",
        "Wishlist disappears when I log out and log back in, very frustrating.",
        "Good app but the sizing recommendations are always a size too big for me.",
        "Love the UI but checking out takes forever and fails sometimes.",
        "I need a better way to filter by exact measurements, standard sizes are wrong.",
        "Why can't I share my wishlist with friends easily?",
        "Post-purchase return process for wrong sizes is annoying.",
        "Please fix the bug where items in cart show as out of stock only at payment.",
        "Great collection, but sizing varies wildly between brands with no warning."
    ],
    "YOUTUBE": [
        "I totally agree with the sizing part, I ordered a M and it fits like an XL!",
        "The haul is great but I wish Myntra would standardise their size charts.",
        "Did anyone else have issues with the cart glitching when adding these items?",
        "I always use the wishlist as a moodboard because I'm scared the fit will be wrong.",
        "Thanks for the review! I was about to buy this but the sizing seems too risky.",
        "Myntra needs to add virtual try-ons, it's 2026!",
        "The return policy for incorrect fits has become so strict lately.",
        "Beautiful pieces, but the sizing is definitely inconsistent across brands here."
    ],
    "TWITTER": [
        "Does anyone else's Myntra cart just randomly empty itself? #myntra",
        "Myntra sizing is a guessing game at this point. Ordered 3 sizes to be safe.",
        "Wishlist full of things I want but I have no idea if they'll actually fit me.",
        "Why is it so hard to find accurate size guides on @myntra?",
        "The anxiety of ordering shoes online because the sizing is never right.",
        "I literally use my Myntra wishlist as therapy.",
        "Can @myntra please fix the checkout bug? My cart is stuck.",
        "Returning clothes because the size chart lied to me again."
    ],
    "INSTAGRAM": [
        "Omg I need this but I'm so worried about the sizing! Is it true to size?",
        "I added this to my wishlist immediately 😍",
        "How does the fit compare to Zara?",
        "I bought this last week and had to return it because the sizing was completely off.",
        "My cart is so full right now but I can't decide on the sizes.",
        "Love this look! Does the app have a proper size guide for this brand?",
        "Wish they had better fit recommendations on the app.",
        "Gorgeous! Adding to my wishlist now."
    ]
}

async def get_or_create_datasource(db, platform: str) -> str:
    result = await db.execute(select(DataSource).filter(DataSource.platform == platform))
    ds = result.scalars().first()
    if not ds:
        ds = DataSource(platform=platform, source_type="api", description=f"Mock data from {platform}")
        db.add(ds)
        await db.commit()
        await db.refresh(ds)
    return ds.id

async def seed_missing():
    print("🌱 Seeding missing sources with realistic data...")
    async with AsyncSessionLocal() as db:
        for platform, comments in MOCK_DATA.items():
            source_id = await get_or_create_datasource(db, platform)
            
            new_items = 0
            for text in comments:
                content_hash = Normalizer.generate_content_hash(text, platform, str(datetime.utcnow().timestamp()) + text)
                
                result = await db.execute(select(FeedbackItem).filter(FeedbackItem.content_hash == content_hash))
                if not result.scalars().first():
                    item = FeedbackItem(
                        source_id=source_id,
                        original_text=text,
                        content_hash=content_hash,
                        source_platform=platform,
                        source_date=datetime.utcnow(),
                        author_id_anonymized=f"mock_user_{uuid.uuid4().hex[:8]}"
                    )
                    db.add(item)
                    new_items += 1
            
            await db.commit()
            print(f"✅ Stored {new_items} items for {platform}")

if __name__ == "__main__":
    asyncio.run(seed_missing())
