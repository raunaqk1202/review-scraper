import os
# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException
from dotenv import load_dotenv
load_dotenv()

from app.api.deps import get_chroma_client
from app.schemas.research import ResearchQueryRequest, ResearchQueryResponse
from app.schemas.opportunity import AISignalResponse

# pyrefly: ignore [missing-import]
import instructor
from groq import AsyncGroq

router = APIRouter()

groq_client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))
client = instructor.from_groq(groq_client, mode=instructor.Mode.JSON)
MODEL_NAME = os.environ.get("GROQ_MODEL", "llama-3.1-70b-versatile")

@router.post("/ask", response_model=ResearchQueryResponse)
async def ask_research_question(
    request: ResearchQueryRequest,
    chroma_client = Depends(get_chroma_client)
):
    """
    RAG Endpoint: Uses ChromaDB to find relevant behavioral signals 
    and Groq LLM to synthesize an answer.
    """
    # Safely get or create the collection
    collection = chroma_client.get_or_create_collection(
        name="behavioral_signals",
        metadata={"hnsw:space": "cosine"}
    )
    
    # 1. Retrieve the top 5 most relevant behavioral signals
    results = collection.query(
        query_texts=[request.query],
        n_results=5
    )
    
    context_blocks = []
    sources = []
    
    if not results.get('documents') or not results['documents'] or not results['documents'][0]:
        # Fallback: if Chroma is empty (e.g., pipeline hasn't run yet), get recent raw feedback items from Postgres
        from app.db.session import AsyncSessionLocal
        from app.models.feedback import FeedbackItem
        from sqlalchemy import select
        
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(FeedbackItem).limit(10))
            recent_items = result.scalars().all()
            
            for i, item in enumerate(recent_items, 1):
                context_blocks.append(f"--- User Feedback {i} ---\n{item.cleaned_text or item.original_text}")
                # We mock a source since we are pulling raw feedback instead of AI signals
                sources.append(AISignalResponse(
                    id=item.id,
                    journey_stage="UNKNOWN",
                    signal_type="RAW_FEEDBACK",
                    confidence_score=1.0
                ))
    else:
        retrieved_docs = results['documents'][0]
        retrieved_metadatas = results['metadatas'][0]
        retrieved_ids = results['ids'][0]
        
        for i in range(len(retrieved_docs)):
            doc_text = retrieved_docs[i]
            meta = retrieved_metadatas[i]
            signal_id = retrieved_ids[i]
            
            context_blocks.append(f"--- User Feedback {i+1} ---\n{doc_text}")
            
            sources.append(AISignalResponse(
                id=signal_id,
                journey_stage=meta.get("journey_stage"),
                signal_type=meta.get("signal_type"),
                confidence_score=meta.get("confidence_score")
            ))
        
    full_context = "\n\n".join(context_blocks)
    
    # 2. Generate the Answer using Groq
    system_prompt = (
        "You are a UX/Consumer Psychology Researcher. Answer the user's question based ONLY "
        "on the retrieved user feedback signals provided below. Do not hallucinate external information. "
        "When quoting or referencing user feedback, always enclose the user's exact words in double quotes (\"). Do not use any brackets or markdown blockquotes for the quotes. "
        "Never include internal IDs, UUIDs, or irrelevant metadata in your response. "
        "If the user's question is random, gibberish, or completely unrelated to UX, consumer psychology, or the retrieved signals, "
        "politely inform them that you didn't understand and ask them to try asking something relatable to the data."
    )
    
    user_prompt = f"Question: {request.query}\n\nRetrieved Signals:\n{full_context}"
    
    try:
        from pydantic import BaseModel
        class LLMAnswer(BaseModel):
            answer: str
            
        ai_response = await client.chat.completions.create(
            model=MODEL_NAME,
            response_model=LLMAnswer,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2
        )
        answer_text = ai_response.answer
    except Exception as e:
        answer_text = f"Error generating answer: {str(e)}"
        
    return ResearchQueryResponse(
        query=request.query,
        answer=answer_text,
        sources=sources
    )
