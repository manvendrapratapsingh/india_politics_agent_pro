.PHONY: help install dev-install test test-cov lint format clean docker-build docker-run

# Default target
help:
	@echo "India Politics Agent Pro - Make Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install        Install production dependencies"
	@echo "  make dev-install    Install development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make format         Format code with black and isort"
	@echo "  make lint           Run linters (flake8, mypy)"
	@echo "  make test           Run unit tests"
	@echo "  make test-cov       Run tests with coverage report"
	@echo "  make test-all       Run all tests including integration"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build   Build Docker image"
	@echo "  make docker-run     Run Docker container"
	@echo "  make docker-compose Start all services with docker-compose"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean          Clean build artifacts and cache"
	@echo "  make pre-commit     Install pre-commit hooks"

# Installation
install:
	pip install -r requirements-new.txt
	pip install -e .

dev-install: install
	pip install -e ".[dev]"
	pre-commit install

# Code Quality
format:
	black src/ tests/ --line-length=120
	isort src/ tests/ --profile black --line-length=120

lint:
	flake8 src/ tests/ --max-line-length=120 --extend-ignore=E203,W503
	mypy src/ --ignore-missing-imports

# Testing
test:
	pytest tests/unit/ -v

test-cov:
	pytest tests/ -v --cov=src/india_politics_agent --cov-report=html --cov-report=term

test-all:
	pytest tests/ -v --cov=src/india_politics_agent --cov-report=html

# Docker
docker-build:
	docker build -t india-politics-agent:latest .

docker-run:
	docker run --rm -it \
		-e GEMINI_API_KEY=${GEMINI_API_KEY} \
		-v $(PWD)/outputs:/app/outputs \
		india-politics-agent:latest

docker-compose:
	docker-compose up -d
	docker-compose logs -f

docker-down:
	docker-compose down -v

# Maintenance
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	rm -rf build/ dist/

pre-commit:
	pre-commit install
	pre-commit run --all-files

# Run agent
run:
	python -m india_politics_agent.cli.main $(ARGS)

# Quick test run
quick-test:
	python -m india_politics_agent.cli.main analyze "Bihar elections 2025" --output outputs/test.md
