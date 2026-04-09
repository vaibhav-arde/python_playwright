<div align="center">
  <h1>🎭 Playwright Pytest Hybrid Framework</h1>
  <p>A robust, scalable, and enterprise-grade test automation framework built with Python, Playwright, and Pytest.</p>

  <!-- Badges -->
  <p>
    <img src="https://img.shields.io/badge/Python-3.13+-blue.svg" alt="Python Version" />
    <img src="https://img.shields.io/badge/Playwright-1.58+-green.svg" alt="Playwright Version" />
    <img src="https://img.shields.io/badge/Pytest-9.0+-yellow.svg" alt="Pytest Version" />
    <img src="https://img.shields.io/badge/Code%20Style-Ruff-black.svg" alt="Ruff Formatter" />
    <img src="https://img.shields.io/badge/License-MIT-success.svg" alt="License" />
  </p>
</div>

## 📖 Overview

This is an architect-level Hybrid Testing Framework designed for both UI and API layer testing. It leverages the speed and reliability of **Microsoft Playwright** and the rich ecosystem of **Pytest**, enabling fast, data-driven, and highly scalable test execution.

### Key Features
- **Hybrid Automation**: Utilize API calls to inject test data and drastically speed up UI test execution.
- **Page Object Model (POM)**: Strict separation of locators, native actions, and high-level page logic.
- **Data-Driven Testing**: Seamless parsing of JSON, CSV, and Excel configurations.
- **Built-in Parallelization**: Run tests concurrently across workers using `pytest-xdist`.
- **Auto-Retries**: Handled via `pytest-rerunfailures` to prevent flaky pipeline failures.
- **Rich Reporting**: Integrates tightly with **Allure Reports** providing screenshots, tracing, and videos upon failure.
- **Strict Quality Gates**: Static analysis and auto-formatting handled entirely by `Ruff` and `mypy` within `pre-commit` hooks.

---

## 🚀 Getting Started

### Prerequisites
- [uv](https://github.com/astral-sh/uv) (Extremely fast Python package installer and resolver)
- Python 3.13+

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vaibhav-arde/python_playwright.git
   cd python_playwright
   ```

2. **Sync the environment and install dependencies**
   ```bash
   uv sync
   ```

3. **Install Playwright Browsers**
   ```bash
   uv run playwright install
   ```

---

## 🏃‍♂️ Running Tests

This framework uses the `uv run pytest` CLI. For default behaviors, please see the `pytest.ini`.

| Execution Type | Command |
| --- | --- |
| **Run all UI Tests (Headless)** | `uv run pytest` |
| **Run tests in Headed UI Mode** | `uv run pytest --headed` |
| **Run tests on a specific browser** | `uv run pytest --browser=firefox` |
| **Run tests matching a Pytest Marker**| `uv run pytest -m "sanity or regression"` |
| **Run in parallel (Auto Workers)** | `uv run pytest -n auto` |
| **Run and generate an Allure Report** | `uv run pytest --alluredir=reports/allure-results` |

---

## 📂 Architecture & Directory Structure

```plaintext
pythonPlaywright/
├── .github/                   ← CI/CD Workflows & Issue Templates
├── api_clients/               ← API wrapper classes (BaseAPI)
├── fixtures/                  ← Custom fixtures avoiding conftest pollution
├── pages/                     ← Page Object Model (POM) classes
├── test_data/                 ← External parametrized data (JSON/CSV/Excel)
├── tests/                     ← Test suites organized by UI and API
├── utils/                     ← Static helpers, messages, config, and DataLoaders
├── reports/                   ← Generated test outputs (HTML + Allure)
├── pytest.ini                 ← Core runtime configurations
├── pyproject.toml             ← Tool constraints & dependency definitions
└── Notes/                     ← In-depth SDET Architectural Documentation
```

> **Note:** For deep-dive framework design rules, specifically regarding where to establish variables vs POM abstractions, please read [Framework Documentation](Notes/Framework_Documentation.md).

---

## 🛠 Pre-commit & Code Quality
Before pushing any code, verify nothing breaks our strict static analysis requirements:
```bash
uv run ruff check .           # Linting
uv run ruff format .          # Code Formatting
uv run mypy .                 # Static Type Checking
```

## 🤝 Contributing
Please see our [Contributing Guidelines](CONTRIBUTING.md) to get started on submitting an issue or a Pull Request. We expect all PRs to pass CI, Ruff, and Mypy checks.

## 📄 License
This project is properly licensed under the [MIT License](LICENSE).
