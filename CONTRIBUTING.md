# Contributing to this Playwright Framework

First off, thank you for considering contributing to this framework!

## 1. Local Development Setup
1. Clone the repository
2. Install dependencies using `uv sync`
3. Install Playwright browsers: `uv run playwright install`

## 2. Before Opening a Pull Request
Please ensure your code passes our CI checks locally before submitting:
- **Linting**: Run `uv run ruff check .`
- **Formatting**: Run `uv run ruff format .`
- **Type Checking**: Run `uv run mypy .`
- **Tests**: Run the test suite `uv run pytest` to ensure no existing flows are broken.

## 3. Branching Strategy
- Branch from `dev`. Do not push directly to `main`.
- Use descriptive branch names e.g., `feature/add-login-tests` or `bugfix/fix-checkout-timeout`.
