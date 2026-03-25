.PHONY: setup dev test lint format check clean

## Setup development environment
setup:
	uv venv && uv sync --group dev && uv run pre-commit install

## Start local development (postgres + server)
dev:
	docker compose -f docker-compose.local.yml up -d postgres && \
	sleep 2 && \
	uv run alembic upgrade head && \
	uv run python run_server_local.py

## Start worker locally
worker:
	uv run python run_worker_local.py

## Run all tests
test:
	uv run pytest tests/ -v

## Run tests with coverage
test-cov:
	uv run pytest tests/ -v --cov=src --cov-report=term-missing

## Run linter
lint:
	uv run ruff check src/

## Run formatter
format:
	uv run ruff format src/

## Run all checks (lint + format check + tests)
check:
	uv run ruff check src/ && \
	uv run ruff format --check src/ && \
	uv run pytest tests/ -v

## Run pre-commit on all files
pre-commit:
	uv run pre-commit run --all-files

## Run database migrations
migrate:
	uv run alembic upgrade head

## Generate new migration
migration:
	@read -p "Migration message: " msg; \
	uv run alembic revision --autogenerate -m "$$msg"

## Clean up
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; \
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null; \
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null; \
	rm -rf .coverage htmlcov/
