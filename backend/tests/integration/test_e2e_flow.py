import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_api_e2e_flow(client):
    # Test 1: Fetch sources
    response = client.get("/api/v1/ingest/sources")
    assert response.status_code == 200
    
    # Test 2: Fetch opportunities
    response = client.get("/api/v1/opportunities")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
    # Test 3: Trigger ingestion (Mocked)
    ingest_payload = {"platform": "TEST", "limit": 5}
    response = client.post("/api/v1/ingest/", json=ingest_payload)
    assert response.status_code in [200, 202]
    
    # Test 4: Research query (Assuming mocked LLM via client dependency if needed)
    research_payload = {"query": "What are the common issues with sizing?"}
    response = client.post("/api/v1/research/ask", json=research_payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
