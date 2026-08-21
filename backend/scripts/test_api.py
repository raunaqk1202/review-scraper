import requests

def test_opportunities():
    print("Testing GET /api/v1/opportunities...")
    response = requests.get("http://localhost:8000/api/v1/opportunities")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {len(data)} opportunities.")
        for opp in data:
            score = opp.get('score', {})
            print(f" - {opp['title']} (ROI Score: {score.get('composite_score')})")
    else:
        print(response.text)

def test_research_ask():
    print("\nTesting POST /api/v1/research/ask...")
    payload = {
        "query": "What are users saying about sizing and return policies?"
    }
    response = requests.post("http://localhost:8000/api/v1/research/ask", json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Query: {data['query']}")
        print(f"Answer: {data['answer']}")
        print(f"Sources cited: {len(data['sources'])}")
    else:
        print(response.text)

if __name__ == "__main__":
    test_opportunities()
    test_research_ask()
