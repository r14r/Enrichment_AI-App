# Configuration
fldr_pages  := "views"


# Default recipe - show available commands
default:
    @just --list

# Install all development dependencies
install:
    uv pip install ruff black isort mypy pylint pytest pytest-cov

# Format code with black
fmt:
    black {{fldr_pages}}

# Sort imports with isort
sort:
    isort {{fldr_pages}}

# Format and sort (combination)
format: sort fmt
    @echo "Code formatted and imports sorted"

# Check code with ruff (fast linter)
ruff:
    ruff check {{fldr_pages}} 

# Fix auto-fixable ruff issues
ruff-fix:
    ruff check --fix {{fldr_pages}} 

# Type check with mypy
types:
    mypy {{fldr_pages}}

# Lint with pylint
pylint:
    pylint {{fldr_pages}}

# Run all checks (formatting, linting, types)
check: ruff types
    @echo "All checks passed"

# Run all checks including pylint (more thorough)
check-all: ruff types pylint
    @echo "All checks including pylint passed"

# Fix all auto-fixable issues
fix: ruff-fix format
    @echo "Auto-fixes applied"

# Run tests
test:
    pytest  -v

# Run tests with coverage
test-cov:
    pytest  --cov={{fldr_pages}} --cov-report=html --cov-report=term

# Clean build artifacts and caches
clean:
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete
    rm -rf htmlcov .coverage

# Complete workflow: fix, check, test
all: fix check test
    @echo "Complete workflow finished successfully"

# Watch mode - run checks on file changes (requires entr)
watch:
    find {{fldr_pages}}  -name "*.py" | entr -c just check

# Pre-commit checks (what CI would run)
ci: format check-all test-cov
    @echo "CI checks complete"


run:
	streamlit run App.py

