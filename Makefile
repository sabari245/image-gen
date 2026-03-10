.PHONY: dev backend frontend install clean

# Run both backend and frontend, open browser
dev:
	@echo "Starting backend and frontend..."
	@trap 'kill 0' EXIT; \
	uv run uvicorn api.main:app --reload --port 8000 & \
	sleep 1 && (cd web && bun dev) & \
	sleep 2 && xdg-open http://localhost:5173 2>/dev/null || open http://localhost:5173 2>/dev/null || true; \
	wait

# Run backend only
backend:
	uv run uvicorn api.main:app --reload --port 8000

# Run frontend only
frontend:
	cd web && bun dev

# Install all dependencies
install:
	uv sync
	cd web && bun install

# Clean generated files
clean:
	rm -rf storage/inputs/* storage/outputs/* storage/generations.db
	rm -rf web/dist
