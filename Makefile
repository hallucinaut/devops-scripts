# DevOps Scripts Makefile
# Simplified commands for common operations

.PHONY: help test all-tests docker test-docker build docker-build run-scripts security-audit docker-security-audit docs

# Help
help:
	@echo "DevOps Scripts - Available Commands"
	@echo "====================================="
	@echo ""
	@echo "Development:"
	@echo "  make test          - Run all unit tests"
	@echo "  make all-tests     - Run all tests with verbose output"
	@echo "  make security-audit - Run security audit on codebase"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run Docker container"
	@echo "  make test-docker   - Run tests in Docker container"
	@echo "  make security-audit-docker - Run security audit in Docker"
	@echo "  make docker-compose-up  - Start all services with docker-compose"
	@echo ""
	@echo "Scripts:"
	@echo "  make run-scripts   - Show available scripts and examples"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs          - Show documentation files"
	@echo ""

# Development commands
test:
	@python3 tests/test_all.py

all-tests:
	@python3 tests/test_all.py -v

security-audit:
	@python3 scripts/security_audit.py --scan directory --directory .

# Docker commands
docker-build:
	@docker build -t devops-scripts:test .

docker-run:
	@docker run --rm -it \
		-v $(shell pwd):/app \
		-v logs:/app/logs \
		-v backups:/app/backups \
		-w /app \
		devops-scripts:test

test-docker:
	@docker build -t devops-scripts:test . && \
		docker run --rm -it \
			-v $(shell pwd):/app \
			-v logs:/app/logs \
			-v backups:/app/backups \
			-w /app \
			devops-scripts:test \
			python3 tests/test_all.py

security-audit-docker:
	@docker build -t devops-scripts:test . && \
		docker run --rm -it \
			-v $(shell pwd):/app \
			-v logs:/app/logs \
			-v backups:/app/backups \
			-w /app \
			devops-scripts:test \
			python3 scripts/security_audit.py --scan directory --directory .

docker-compose-up:
	@echo "Starting all services with docker-compose..."
	@docker-compose up -d

docker-compose-down:
	@echo "Stopping all services..."
	@docker-compose down

# Scripts
run-scripts:
	@bash scripts/run.sh

# Documentation
docs:
	@echo "Documentation files:"
	@ls -1 docs/

# Clean
clean:
	@rm -rf __pycache__ scripts/__pycache__ tests/__pycache__ *.pyc scripts/*.pyc tests/*.pyc
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleaned Python cache files"

# Build requirements
install-requirements:
	@pip install -r requirements.txt
