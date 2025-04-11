# Makefile: LLM OS Project Launcher

# Backend and frontend ports
BACKEND_PORT=8000
FRONTEND_PORT=5173

# Default: start both backend and frontend (sequentially)
run: backend frontend

# Start FastAPI backend
backend:
	@echo "🚀 Starting backend at http://localhost:$(BACKEND_PORT)..."
	@cd ./ && uvicorn endpoints:app --reload --port $(BACKEND_PORT)

# Start React frontend using Vite
frontend:
	@echo "🌐 Starting frontend at http://localhost:$(FRONTEND_PORT)..."
	@cd frontend && npm run dev

# Install frontend dependencies
install-frontend:
	@cd frontend && npm install

# Install + Run
start:
	make install-frontend
	make run

# Clean Python cache files
clean:
	find . -type d -name '__pycache__' -exec rm -r {} +
