.PHONY: setup up down migrate seed test

setup:
	@echo "Setting up Discovery Engine..."
	mkdir -p data/chroma
	touch data/discovery_engine.db
	@echo "Setup complete. Next steps:"
	@echo "1. Create virtual environment for backend and install dependencies."
	@echo "2. Install frontend dependencies."
	@echo "3. Run 'make migrate'."

up:
	@echo "To run the application locally without Docker, start two terminals:"
	@echo "Terminal 1 (Backend): cd backend && uvicorn app.main:app --reload --port 8000"
	@echo "Terminal 2 (Frontend): cd frontend && npm run dev"

migrate:
	cd backend && alembic upgrade head

seed:
	cd backend && python -m app.scripts.seed

test:
	cd backend && pytest
