import os
import instructor
from groq import AsyncGroq
from app.services.schemas import NoiseReductionResult, SignalExtractionResult

# Initialize the instructor-patched AsyncGroq client for guaranteed JSON schema output
groq_client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))
client = instructor.from_groq(groq_client, mode=instructor.Mode.JSON)

# We use Qwen for deep psychological extraction
MODEL_NAME = "qwen/qwen3.6-27b"

async def filter_noise(text: str) -> NoiseReductionResult:
    return await client.chat.completions.create(
        model=MODEL_NAME,
        response_model=NoiseReductionResult,
        messages=[
            {"role": "system", "content": "You are an expert consumer psychologist. Analyze the text. Is it a genuine discussion about fashion shopping behaviors (wishlists, comparing items, fit/sizing, postponement, intent)? Or is it spam/generic app bug complaining?"},
            {"role": "user", "content": text}
        ],
        temperature=0.0,
    )

async def extract_signals(text: str) -> SignalExtractionResult:
    return await client.chat.completions.create(
        model=MODEL_NAME,
        response_model=SignalExtractionResult,
        messages=[
            {"role": "system", "content": "You are an expert consumer psychologist analyzing fashion e-commerce. Extract specific psychological insights, purchase barriers, unmet needs, or behavioral patterns (like how they use wishlists or compare items). Do not extract generic sentiment. Be highly specific."},
            {"role": "user", "content": text}
        ],
        temperature=0.1,
    )
