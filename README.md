# AI-Powered Fashion Purchase Discovery Intelligence Engine

An automated system to ingest, clean, and enrich fashion feedback data to surface actionable product opportunities.

## Quick Start

### 1. Requirements
- Python 3.9+
- Node.js 18+
- SQLite (built-in)

### 2. Setup Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env # Configure GROQ_API_KEY
make migrate
```

### 3. Setup Frontend
```bash
cd frontend
npm install
npm run dev
```

### 4. Run the Pipeline
Once services are running, trigger data ingestion and the AI pipeline:
```bash
curl -X POST http://localhost:8000/api/v1/pipeline/run
```

## Architecture Summary
- **Backend:** FastAPI, SQLAlchemy, SQLite, ChromaDB for semantic search.
- **Frontend:** Next.js, React, TailwindCSS.
- **AI Pipeline:** Uses Groq LLM to classify intent, extract barriers, cluster semantically, and generate ranked opportunities.

## Demo Flow
1. **Ingest Data:** Seed data is loaded from sample sources or APIs.
2. **AI Enrichment:** The pipeline categorizes and semantically groups the feedback.
3. **Discover:** The Next.js dashboard visualizes the ranked opportunities.
4. **Chat:** PMs can ask natural-language questions to the research engine via the dashboard chat.
