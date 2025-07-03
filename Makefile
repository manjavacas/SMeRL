# SMeRL Makefile
# Commands to manage the SMeRL project

.PHONY: help run clean clean-eplus clean-cache clean-all install test lint format check setup download-eplus install-eplus check-eplus

# Variables
PYTHON := python3
PIP := pip3
POETRY := poetry
EPLUS_DIRS := Eplus-*
CACHE_DIRS := __pycache__ .pytest_cache .mypy_cache
SCRIPT_DIR := scripts
EPLUS_PATH := EnergyPlus-24-1-0
EPLUS_URL := https://github.com/NREL/EnergyPlus/releases/download/v24.1.0/EnergyPlus-24.1.0-9d7789a3ac-Linux-Ubuntu22.04-x86_64.run
EPLUS_INSTALLER := EnergyPlus-24.1.0-9d7789a3ac-Linux-Ubuntu22.04-x86_64.run

# Default command
.DEFAULT_GOAL := help

help: ## Show this help
	@echo "SMeRL - Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

run: ## Execute the main script with EnergyPlus environment
	@echo "Setting up EnergyPlus environment and running scripts/run.py..."
	@export EPLUS_PATH=$(EPLUS_PATH) && \
	 export PYTHONPATH=$(EPLUS_PATH) && \
	 $(POETRY) run python $(SCRIPT_DIR)/run.py

run-script: ## Execute the Python script in scripts/run.py
	@echo "Running scripts/run.py..."
	@cd $(SCRIPT_DIR) && $(PYTHON) run.py

run-test: ## Execute the test script with Pendulum test environment
	@echo "Setting up Pendulum test environment and running scripts/run_test.py..."
	@$(POETRY) run python $(SCRIPT_DIR)/run_test.py

clean-eplus: ## Clean all Eplus-* directories
	@echo "Cleaning Eplus-* directories..."
	@rm -rf $(EPLUS_DIRS)
	@echo "Eplus-* directories removed."

clean-cache: ## Clean Python cache files
	@echo "Cleaning cache files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@find . -name "*.pyo" -delete 2>/dev/null || true
	@echo "Cache cleaned."

clean-logs: ## Clean log files
	@echo "Cleaning log files..."
	@find . -name "*.log" -delete 2>/dev/null || true
	@find . -name "*.out" -delete 2>/dev/null || true
	@echo "Logs removed."

clean: clean-cache clean-logs ## Basic cleanup (cache and logs)

clean-all: clean clean-eplus ## Complete cleanup (cache, logs and Eplus directories)
	@echo "Complete cleanup done."

download-eplus: ## Download EnergyPlus installer
	@echo "Downloading EnergyPlus 24.1.0..."
	@if [ -f "$(EPLUS_INSTALLER)" ]; then \
		echo "EnergyPlus installer already exists."; \
	else \
		wget -O $(EPLUS_INSTALLER) $(EPLUS_URL); \
		echo "EnergyPlus installer downloaded."; \
	fi

install-eplus: download-eplus ## Install EnergyPlus in project directory
	@echo "Installing EnergyPlus..."
	@if [ -d "$(EPLUS_PATH)" ]; then \
		echo "EnergyPlus already installed in $(EPLUS_PATH)"; \
	else \
		chmod +x $(EPLUS_INSTALLER); \
		./$(EPLUS_INSTALLER) --skip-license --prefix=./$(EPLUS_PATH); \
		echo "EnergyPlus installed successfully in $(EPLUS_PATH)"; \
		rm -f $(EPLUS_INSTALLER); \
		echo "Installer removed."; \
	fi

check-eplus: ## Check if EnergyPlus is installed
	@echo "Checking EnergyPlus installation..."
	@if [ -d "$(EPLUS_PATH)" ]; then \
		echo "✓ EnergyPlus found in $(EPLUS_PATH)"; \
		ls -la $(EPLUS_PATH)/energyplus 2>/dev/null || echo "  Warning: energyplus executable not found"; \
	else \
		echo "✗ EnergyPlus not found. Run 'make install-eplus' to install it."; \
	fi

install: ## Install dependencies using Poetry
	@echo "Installing dependencies..."
	@$(POETRY) install
	@echo "Dependencies installed."

install-dev: ## Install development dependencies
	@echo "Installing development dependencies..."
	@$(POETRY) install --with dev
	@echo "Development dependencies installed."

update: ## Update dependencies
	@echo "Updating dependencies..."
	@$(POETRY) update
	@echo "Dependencies updated."

shell: ## Open Poetry shell
	@$(POETRY) shell

test: ## Run tests
	@echo "Running tests..."
	@$(POETRY) run pytest -v
	@echo "Tests completed."

test-coverage: ## Run tests with coverage
	@echo "Running tests with coverage..."
	@$(POETRY) run pytest --cov=smerl --cov-report=html --cov-report=term
	@echo "Tests with coverage completed."

lint: ## Run linting with flake8
	@echo "Running linting..."
	@$(POETRY) run flake8 smerl/ scripts/
	@echo "Linting completed."

format: ## Format code with black
	@echo "Formatting code..."
	@$(POETRY) run black smerl/ scripts/
	@echo "Code formatted."

format-check: ## Check format without making changes
	@echo "Checking format..."
	@$(POETRY) run black --check smerl/ scripts/
	@echo "Format check completed."

type-check: ## Check types with mypy
	@echo "Checking types..."
	@$(POETRY) run mypy smerl/
	@echo "Type check completed."

check: lint format-check type-check ## Run all checks

setup: install ## Initial project setup
	@echo "Setting up project..."
	@echo "Project configured successfully."

docs: ## Generate documentation
	@echo "Generating documentation..."
	@$(POETRY) run sphinx-build -b html docs/ docs/_build/html
	@echo "Documentation generated in docs/_build/html/"

serve-docs: docs ## Serve documentation locally
	@echo "Serving documentation at http://localhost:8000"
	@cd docs/_build/html && $(PYTHON) -m http.server 8000

env-info: ## Show environment information
	@echo "Environment information:"
	@echo "Python: $$($(PYTHON) --version)"
	@echo "Poetry: $$($(POETRY) --version)"
	@echo "Working directory: $$(pwd)"
	@echo "Git branch: $$(git branch --show-current 2>/dev/null || echo 'No git repo')"
	@echo "Git status: $$(git status --porcelain 2>/dev/null | wc -l) files modified"

list-eplus: ## List all Eplus-* directories
	@echo "Found Eplus directories:"
	@ls -la | grep "^d.*Eplus-" || echo "No Eplus-* directories found"

backup: ## Create source code backup
	@echo "Creating backup..."
	@tar -czf backup_$$(date +%Y%m%d_%H%M%S).tar.gz \
		--exclude='$(EPLUS_DIRS)' \
		--exclude='__pycache__' \
		--exclude='.git' \
		--exclude='*.pyc' \
		--exclude='*.log' \
		.
	@echo "Backup created."

# Quick development commands
dev: clean install-dev ## Quick development setup
	@echo "Development environment ready."

quick-test: ## Quick test (only modified files)
	@echo "Running quick tests..."
	@$(POETRY) run pytest -x --lf
	@echo "Quick tests completed."

# Command to view project status
status: env-info list-eplus ## Show complete project status
	@echo ""
	@echo "SMeRL Project Status:"
	@echo "===================="
