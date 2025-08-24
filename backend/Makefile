# AI Challenge Backend Test Makefile

.PHONY: help install test test-unit test-integration test-flaky test-coverage test-parallel test-verbose clean

# Variables
PYTHON := python3
PIP := pip3
PYTEST := pytest
TEST_DIR := tests

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install test dependencies
	$(PIP) install -r test-requirements.txt

test: ## Run all tests
	$(PYTEST) $(TEST_DIR) -v

test-unit: ## Run only unit tests
	$(PYTEST) $(TEST_DIR) -v -m "unit"

test-integration: ## Run only integration tests  
	$(PYTEST) $(TEST_DIR) -v -m "integration"

test-bdd: ## Run BDD (Given-When-Then) tests
	$(PYTEST) $(TEST_DIR) -v -k "bdd"

test-table-driven: ## Run table-driven tests
	$(PYTEST) $(TEST_DIR) -v -k "table_driven"

test-flaky: ## Run flaky tests with retry
	$(PYTEST) $(TEST_DIR) -v -m "flaky"

test-no-flaky: ## Run tests excluding flaky ones
	$(PYTEST) $(TEST_DIR) -v -m "not flaky"

test-slow: ## Run slow tests
	$(PYTEST) $(TEST_DIR) -v -m "slow"

test-fast: ## Run fast tests (exclude slow)
	$(PYTEST) $(TEST_DIR) -v -m "not slow"

test-coverage: ## Run tests with coverage report
	$(PYTEST) $(TEST_DIR) -v --cov=. --cov-report=term-missing --cov-report=html:htmlcov

test-parallel: ## Run tests in parallel (auto-detect CPU cores)
	$(PYTEST) $(TEST_DIR) -v -n auto

test-parallel-4: ## Run tests in parallel with 4 workers
	$(PYTEST) $(TEST_DIR) -v -n 4

test-verbose: ## Run tests with maximum verbosity
	$(PYTEST) $(TEST_DIR) -vvv -s

test-interview: ## Run interview service tests only
	$(PYTEST) $(TEST_DIR)/interview-service -v

test-learning: ## Run learning service tests only
	$(PYTEST) $(TEST_DIR)/learning-service -v

test-resume: ## Run resume service tests only
	$(PYTEST) $(TEST_DIR)/resume-service -v

test-timeout: ## Run tests with 30s timeout
	$(PYTEST) $(TEST_DIR) -v --timeout=30

test-debug: ## Run specific test with debugging
	$(PYTEST) $(TEST_DIR) -v -s --pdb

test-failed: ## Re-run only failed tests
	$(PYTEST) $(TEST_DIR) -v --lf

test-new: ## Run only new/modified tests
	$(PYTEST) $(TEST_DIR) -v --ff

clean: ## Clean test artifacts
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf __pycache__
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

# Service-specific test combinations
test-interview-all: ## Run all interview service test patterns
	@echo "Running Interview Service BDD tests..."
	$(PYTEST) tests/interview-service/test_interview_bdd.py -v
	@echo "Running Interview Service Table-Driven tests..."
	$(PYTEST) tests/interview-service/test_interview_table_driven.py -v
	@echo "Running Interview Service Flaky tests..."
	$(PYTEST) tests/interview-service/test_interview_flaky.py -v

test-learning-all: ## Run all learning service test patterns
	@echo "Running Learning Service BDD tests..."
	$(PYTEST) tests/learning-service/test_learning_path_bdd.py -v

test-ci: ## Run tests for CI/CD (no slow, with coverage)
	$(PYTEST) $(TEST_DIR) -v -m "not slow" --cov=. --cov-report=xml --maxfail=10

test-local: ## Run tests for local development
	$(PYTEST) $(TEST_DIR) -v -x --tb=short

# Example usage:
# make test                    # Run all tests
# make test-interview         # Test only interview service  
# make test-parallel          # Run tests in parallel
# make test-coverage          # Run with coverage report
# make test-no-flaky          # Skip potentially unstable tests
