from pydantic import BaseModel
from typing import List
from .opportunity import AISignalResponse

class ResearchQueryRequest(BaseModel):
    query: str

class ResearchQueryResponse(BaseModel):
    query: str
    answer: str
    sources: List[AISignalResponse]
