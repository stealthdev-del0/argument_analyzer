.PHONY: help install dev test run docker-build docker-run docker-push clean lint format

help:
	@echo "🧠 Argument Structure Analyzer - Development Commands"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install       - Install dependencies"
	@echo "  make dev          - Install dev dependencies"
	@echo ""
	@echo "Running:"
	@echo "  make run          - Run Streamlit app"
	@echo "  make run-cli      - Run CLI demo"
	@echo "  make test         - Run unit tests"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"
	@echo "  make docker-push  - Push to Docker Hub"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code with black"
	@echo "  make clean        - Clean up cache files"
	@echo ""

install:
	pip install -r requirements.txt

dev:
	pip install -r requirements.txt
	pip install pytest pytest-cov black flake8

run:
	streamlit run app.py

run-cli:
	python main.py

test:
	python test_units.py

test-verbose:
	pytest test_units.py -v --tb=short

test-coverage:
	pytest test_units.py --cov=. --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

docker-build:
	docker build -t argument-analyzer:latest .

docker-run:
	docker run -p 8501:8501 argument-analyzer:latest

docker-compose-up:
	docker-compose up

docker-compose-down:
	docker-compose down

docker-push:
	docker push yourusername/argument-analyzer:latest

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

format:
	black .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache htmlcov .coverage
	rm -rf build dist *.egg-info

.DEFAULT_GOAL := help
