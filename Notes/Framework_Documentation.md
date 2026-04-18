# 📘 Python Playwright Hybrid Test Automation Framework

## Documentation

> **Version**: 0.2.0
> **Python**: 3.13 | **Playwright**: 1.58+ | **Pytest**: 9.0+
> **Package Manager**: uv
> **Target Application**: https://tutorialsninja.com/demo/ (OpenCart)

---

## 📑 Table of Contents

1. [Framework Overview](#-1-framework-overview)
2. [Project Structure](#-2-project-structure)
3. [Architecture &amp; Design Principles](#-3-architecture--design-principles)
4. [Technology Stack](#-4-technology-stack)
5. [Core Framework Layer](#-5-core-framework-layer)
6. [Fixtures Layer](#-6-fixtures-layer)
7. [Page Objects Layer](#-7-page-objects-layer)
8. [API Clients Layer](#-8-api-clients-layer)
9. [Utilities Layer](#-9-utilities-layer)
10. [Test Layer](#-10-test-layer)
11. [Test Data Management](#-11-test-data-management)
12. [Configuration Files](#-12-configuration-files)
13. [Reporting](#-13-reporting)
14. [CI/CD Pipeline](#-14-cicd-pipeline)
15. [Code Quality &amp; Linting](#-15-code-quality--linting)
16. [How to Run Tests](#-16-how-to-run-tests)
17. [Dependency Graph](#-17-dependency-graph)
18. [File Reference Index](#-18-file-reference-index)
19. [Strict Engineering Guidelines](#-19-strict-engineering-guidelines)

---

## 🎯 1. Framework Overview

This is a **Senior SDET / Architect level** enterprise test automation framework built with **Playwright + Pytest** following the **Hybrid Testing Pattern** (UI + API).

### Key Capabilities

| Capability            | Implementation                                      |
| --------------------- | --------------------------------------------------- |
| UI Testing            | Playwright browser automation via Page Object Model |
| API Testing           | Playwright APIRequestContext via API Client pattern |
| Hybrid Testing        | API creates data → UI validates → fast + reliable |
| Parallel Execution    | `pytest-xdist` (`-n auto`)                      |
| Retry on Failure      | `pytest-rerunfailures` (`--reruns 2`)           |
| Data-Driven Testing   | JSON / CSV / Excel data sources                     |
| Multi-Browser Support | Chromium, Firefox, WebKit via `--browser`         |
| Reporting             | Allure + HTML Report                                |
| CI/CD                 | GitHub Actions with Playwright Docker container     |
| Code Quality          | Ruff (lint + format), mypy (type check), pre-commit |

---

## 🗂 2. Project Structure

```text
pythonPlaywright/
│
├── conftest.py                 ← Root conftest (REGISTRY ONLY — 3 lines)
├── pytest.ini                  ← Pytest configuration & CLI defaults
├── pyproject.toml              ← Project metadata, dependencies, tool config
├── .python-version             ← Python 3.13 pinned for uv
├── uv.lock                    ← Locked dependency resolution
├── .pre-commit-config.yaml     ← Pre-commit hooks (ruff, mypy)
├── .gitignore                  ← Git ignore rules
├── README.md                   ← Project readme
│
├── fixtures/                   ← 🔧 FIXTURE LOGIC (separated from conftest)
│   ├── __init__.py
│   ├── browser.py              ←   Auto-navigate + screenshot/video on failure
│   ├── api.py                  ←   Session-scoped API context
│   └── auth.py                 ←   Session-scoped auth token
│
├── pages/                      ← 📄 PAGE OBJECTS (UI Layer — POM Pattern)
│   ├── __init__.py
│   ├── base_page.py            ←   BasePage — inherited by all pages
│   ├── home_page.py            ←   Home / search / navigation
│   ├── login_page.py           ←   Login form interactions
│   ├── registration_page.py    ←   Registration form
│   ├── my_account_page.py      ←   Post-login account area
│   ├── logout_page.py          ←   Logout confirmation
│   ├── search_results_page.py  ←   Product search results
│   ├── product_page.py         ←   Single product details
│   ├── shopping_cart_page.py   ←   Cart summary
│   └── checkout_page.py        ←   Full checkout flow
│
├── api_clients/                ← 🌐 API CLIENT ABSTRACTIONS
│   ├── __init__.py
│   └── base_api.py             ←   BaseAPI — inherited by all API clients
│
├── utils/                      ← ⚙️ SHARED UTILITIES
│   ├── __init__.py
│   ├── config.py               ←   Environment-based config + test credentials
│   ├── constants.py            ←   API endpoints, HTTP headers, UI routes
│   ├── logger.py               ←   Centralized Python logging
│   ├── data_loader.py          ←   JSON / CSV / Excel data readers
│   ├── helpers.py              ←   Random data generation (Faker)
│   └── messages.py             ←   UI assertion strings (Toast, Warnings)
│
├── tests/                      ← 🧪 TEST SUITES
│   ├── __init__.py
│   ├── ui/                     ←   UI test suite
│   │   ├── __init__.py
│   │   ├── test_login.py
│   │   ├── test_login_data_driven.py
│   │   ├── test_user_registration.py
│   │   ├── test_user_logout.py
│   │   ├── test_product_search.py
│   │   ├── test_add_product_to_cart.py
│   │   └── test_end_to_end.py
│   └── api/                    ←   API test suite (placeholder)
│       └── __init__.py
│
├── test_data/                  ← 📊 EXTERNAL TEST DATA FILES
│   ├── logindata.json
│   ├── logindata.csv
│   └── logindata.xlsx
│
├── reports/                    ← 📈 GENERATED REPORTS (gitignored)
│   ├── allure-results/
│   ├── screenshots/
│   ├── traces/
│   ├── videos/
│   └── myreport.html
│
├── .github/workflows/          ← 🚀 CI/CD
│   └── playwright.yml
│
└── Notes/                      ← 📝 LEARNING & REFERENCE NOTES
```

---

## 🧠 3. Architecture & Design Principles

### 3.1 Core Design Principles

```text
✔ Separation of Concerns — fixtures, pages, tests, and utils are isolated
✔ No Hardcoding — all values come from config/constants
✔ Reusable Fixtures — modular fixtures registered via conftest.py
✔ Page Object Model (POM) — all UI interaction through page classes
✔ API Client Abstraction — HTTP operations through base/derived API classes
✔ BasePage / BaseAPI Inheritance — DRY common methods
✔ Centralized Authentication — session-scoped token reuse
✔ Data-Driven Testing — external files, not inline values
✔ Scalable & CI/CD Ready — parallel execution, GitHub Actions
```

### 3.2 Layered Architecture

```
┌─────────────────────────────────────────────────┐
│                  TEST LAYER                      │
│    tests/ui/test_*.py  |  tests/api/test_*.py   │
├─────────────────────────────────────────────────┤
│              PAGE OBJECTS / API CLIENTS           │
│   pages/*.py (→ BasePage)  |  api_clients/*.py   │
├─────────────────────────────────────────────────┤
│                FIXTURES LAYER                    │
│   fixtures/browser.py | api.py | auth.py         │
├─────────────────────────────────────────────────┤
│                UTILITIES LAYER                   │
│  config.py | constants.py | logger.py |          │
│  data_loader.py | helpers.py                     │
├─────────────────────────────────────────────────┤
│          CONFTEST.PY (Registry Only)             │
├─────────────────────────────────────────────────┤
│   PYTEST + PLAYWRIGHT + ALLURE (Infrastructure)  │
└─────────────────────────────────────────────────┘
```

### 3.3 Data Flow — Hybrid Test Pattern

```
API creates data → UI validates → fast + reliable

Example:
  1. API: POST /register → creates user
  2. API: POST /login → gets auth token
  3. UI:  Navigate to dashboard → verify user data displayed
```

---

## 🛠 4. Technology Stack

### Runtime Dependencies

| Package                  | Version   | Purpose                       |
| ------------------------ | --------- | ----------------------------- |
| `playwright`           | ≥1.58.0  | Browser automation engine     |
| `pytest`               | ≥9.0.2   | Test runner and framework     |
| `pytest-playwright`    | ≥0.7.2   | Playwright-Pytest integration |
| `pytest-html`          | ≥4.2.0   | HTML test report generation   |
| `pytest-xdist`         | ≥3.5.0   | Parallel test execution       |
| `pytest-rerunfailures` | ≥14.0    | Auto-retry failed tests       |
| `pytest-cov`           | ≥7.0.0   | Code coverage measurement     |
| `allure-pytest`        | ≥2.15.3  | Allure reporting integration  |
| `faker`                | ≥40.11.0 | Random test data generation   |
| `openpyxl`             | ≥3.1.5   | Excel file reading            |
| `jsonschema`           | ≥4.26.0  | JSON schema validation        |

### Dev Dependencies

| Package        | Version  | Purpose                                    |
| -------------- | -------- | ------------------------------------------ |
| `ruff`       | ≥0.15.7 | Linter + formatter (replaces black/flake8) |
| `mypy`       | ≥1.19.1 | Static type checking                       |
| `pre-commit` | ≥4.5.1  | Git pre-commit hook runner                 |

### Package Management

- **`uv`** is used as the package manager (not pip)
- Dependencies declared in `pyproject.toml`
- Lockfile: `uv.lock`
- Virtual environment: `.venv/` (auto-managed by uv)

---

## 🧱 5. Core Framework Layer

### 5.1 BasePage (`pages/base_page.py`)

The **foundation of all Page Objects**. Every page class inherits from `BasePage` and gets:

```python
class BasePage:
    def __init__(self, page: Page)    # Stores Playwright Page instance
    def open(self, path: str)         # Navigate to relative URL
    def click(self, locator: str)     # Click an element by selector
    def fill(self, locator: str, value: str)  # Fill text input
    def get_text(self, locator: str)  # Get inner text
    def is_visible(self, locator: str)  # Check element visibility
    def wait_for(self, locator: str, state, timeout)  # Explicit wait
    def get_title(self) -> str        # Get page title
    def get_url(self) -> str          # Get current URL
```

### 5.2 BaseAPI (`api_clients/base_api.py`)

The **foundation of all API Client classes**. Wraps Playwright's `APIRequestContext`:

```python
class BaseAPI:
    def __init__(self, request, headers=None)  # Stores request context
    def get(self, endpoint, **kwargs)           # GET request
    def post(self, endpoint, **kwargs)          # POST request
    def put(self, endpoint, **kwargs)           # PUT request
    def patch(self, endpoint, **kwargs)         # PATCH request
    def delete(self, endpoint, **kwargs)        # DELETE request
```

**Usage — Creating a new API client:**

```python
from api_clients.base_api import BaseAPI
from utils.constants import APIEndpoints

class BookingAPI(BaseAPI):
    def create_booking(self, payload):
        return self.post(APIEndpoints.BOOKING, data=payload)

    def get_booking(self, booking_id):
        return self.get(f"{APIEndpoints.BOOKING}/{booking_id}")
```

---

## 🔧 6. Fixtures Layer

### Architecture Decision

```text
✔ Fixture LOGIC lives in → fixtures/*.py
✔ conftest.py is REGISTRY ONLY → just imports
```

**conftest.py (root — 3 lines):**

```python
from fixtures.browser import *   # noqa: F401, F403
from fixtures.api import *       # noqa: F401, F403
from fixtures.auth import *      # noqa: F401, F403
```

### 6.1 `fixtures/browser.py`

| Fixture / Hook                | Scope    | Purpose                                                    |
| ----------------------------- | -------- | ---------------------------------------------------------- |
| `pytest_runtest_makereport` | Hook     | Captures pass/fail result on each test phase               |
| `navigate_to_base_url`      | function | Auto-navigates `page` to `--base-url` before each test |
|                               |          | Captures screenshot on failure → attaches to Allure       |
|                               |          | Captures video on failure → attaches to Allure            |

This fixture is `autouse=True`, so **every test automatically** starts at the configured base URL without needing to call `page.goto()`.

### 6.2 `fixtures/api.py`

| Fixture         | Scope   | Purpose                                                  |
| --------------- | ------- | -------------------------------------------------------- |
| `api_context` | session | Creates a Playwright `APIRequestContext` for API tests |

Uses the `API_URL` from `utils/config.py`, keyed by the `ENV` environment variable.

### 6.3 `fixtures/auth.py`

| Fixture        | Scope   | Purpose                                        |
| -------------- | ------- | ---------------------------------------------- |
| `auth_token` | session | Authenticates via API once and returns a token |

Session-scoped so authentication happens **only once per test run**, not before every test.

---

## 📄 7. Page Objects Layer

### Inheritance Chain

```text
BasePage  ←──  HomePage
          ←──  LoginPage
          ←──  RegistrationPage
          ←──  MyAccountPage
          ←──  LogoutPage
          ←──  SearchResultsPage
          ←──  ProductPage
          ←──  ShoppingCartPage
          ←──  CheckoutPage
```

### Page Object Reference

| Page Object           | File                             | Key Responsibilities                               |
| --------------------- | -------------------------------- | -------------------------------------------------- |
| `HomePage`          | `pages/home_page.py`           | My Account dropdown, search box, navigation        |
| `LoginPage`         | `pages/login_page.py`          | Email/password fields, login action, error message |
| `RegistrationPage`  | `pages/registration_page.py`   | Full registration form, privacy policy             |
| `MyAccountPage`     | `pages/my_account_page.py`     | Account heading verification, logout link          |
| `LogoutPage`        | `pages/logout_page.py`         | Continue button after logout                       |
| `SearchResultsPage` | `pages/search_results_page.py` | Product search results, product selection          |
| `ProductPage`       | `pages/product_page.py`        | Quantity, add-to-cart, confirmation, cart nav      |
| `ShoppingCartPage`  | `pages/shopping_cart_page.py`  | Total price, checkout button                       |
| `CheckoutPage`      | `pages/checkout_page.py`       | Guest checkout, billing, shipping, order confirm   |

### Page Object Pattern

Every page object follows this consistent structure:

```python
from pages.base_page import BasePage

class SomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)          # ← inherit BasePage
        self.element = page.locator()   # ← define locators

    def action_method(self):            # ← user interactions
        self.element.click()

    def get_element(self):              # ← return locators for assertions
        return self.element
```

---

## 🌐 8. API Clients Layer

### Current State

| File            | Contents                                         |
| --------------- | ------------------------------------------------ |
| `base_api.py` | `BaseAPI` class with GET/POST/PUT/PATCH/DELETE |
| `__init__.py` | Package initializer                              |

### How to Extend — Adding a new API Client

```python
# api_clients/user_api.py
from api_clients.base_api import BaseAPI
from utils.constants import APIEndpoints

class UserAPI(BaseAPI):
    def create_user(self, payload):
        return self.post(APIEndpoints.USERS, data=payload)

    def get_user(self, user_id):
        return self.get(f"{APIEndpoints.USERS}/{user_id}")
```

**Usage in tests:**

```python
def test_create_user(api_context):
    api = UserAPI(api_context)
    res = api.create_user({"name": "John"})
    assert res.status == 201
```

---

## ⚙️ 9. Utilities Layer

### 9.1 `utils/config.py` — Environment Configuration

```python
ENV = os.getenv("ENV", "qa")          # Switch via: ENV=prod pytest

BASE_URL = {
    "qa":   "https://tutorialsninja.com/demo/",
    "prod": "https://tutorialsninja.com/demo/",
}

API_URL = {
    "qa":   "https://tutorialsninja.com/demo/index.php?route=api",
    "prod": "https://tutorialsninja.com/demo/index.php?route=api",
}

class Config:
    email = "pavanol@abc.com"           # Valid test credentials
    password = "test@123"
    invalid_email = "pavanol123@abc.com" # Invalid test credentials
    invalid_password = "test@123xyz"
    product_name = "MacBook"            # Product test data
    product_quantity = "1"
    total_price = "$602.00"
```

### 9.2 `utils/constants.py` — Centralized Constants

| Class            | Purpose                                            |
| ---------------- | -------------------------------------------------- |
| `APIEndpoints` | API route paths: LOGIN, CART, ORDER, PAYMENT, etc. |
| `Headers`      | Common HTTP headers: JSON, FORM                    |
| `UIRoutes`     | UI route paths: HOME, LOGIN, REGISTER, etc.        |

### 9.3 `utils/messages.py` — Centralized UI Strings

All expected string values used in assertions (e.g., toast messages, validation errors) live here to avoid hardcoding strings in tests.

```python
ACCOUNT_CREATED = "Your Account Has Been Created!"
WARN_PASSWORD = "Password must be between 4 and 20 characters!"
```

### 9.4 `utils/logger.py` — Centralized Logging

```python
from utils.logger import get_logger
logger = get_logger(__name__)
logger.info("Test started")
# Output: 2026-03-21 12:00:00 | INFO     | module_name | Test started
```

### 9.5 `utils/data_loader.py` — Test Data Readers

| Function              | Source    | Returns         |
| --------------------- | --------- | --------------- |
| `read_json_data()`  | `.json` | `list[tuple]` |
| `read_csv_data()`   | `.csv`  | `list[tuple]` |
| `read_excel_data()` | `.xlsx` | `list[tuple]` |

### 9.6 `utils/helpers.py` — Random Data Generation

`RandomDataUtil` class wrapping `Faker`:

```python
random_data = RandomDataUtil()
random_data.get_first_name()           # "John"
random_data.get_email()                # "john.doe@example.com"
random_data.get_password()             # "aB3$kL9mN1"
random_data.get_random_alphanumeric(8) # "aB3kL9mN"
```

---

## 🧪 10. Test Layer

### 10.1 Test Suite Overview

| Test File                       | Markers                    | Description                                    |
| ------------------------------- | -------------------------- | ---------------------------------------------- |
| `test_login.py`               | `regression`, `sanity` | Valid + invalid login scenarios                |
| `test_login_data_driven.py`   | `datadriven`             | Parametrized login from Excel data             |
| `test_user_registration.py`   | `sanity`, `regression` | New user registration with random data         |
| `test_user_logout.py`         | `regression`             | Login → verify → logout → verify home page  |
| `test_product_search.py`      | `sanity`, `regression` | Search for product, verify results             |
| `test_add_product_to_cart.py` | `regression`             | Search → select → set qty → add to cart     |
| `test_end_to_end.py`          | `end_to_end`             | Full flow: register → logout → login → cart |

### 10.2 Test Anatomy

Every test follows this pattern:

```python
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from utils.config import Config

@pytest.mark.regression
def test_example(page):                    # ← page fixture from pytest-playwright
    home_page = HomePage(page)             # ← instantiate Page Object
    home_page.enter_product_name("MacBook") # ← interact via page methods
    home_page.click_search()
    expect(some_locator).to_be_visible()   # ← assert with Playwright expect
```

### 10.3 Custom Markers

| Marker         | Purpose                                |
| -------------- | -------------------------------------- |
| `sanity`     | Quick basic checks (smoke level)       |
| `regression` | Full end-to-end validation             |
| `datadriven` | Parametrized tests using external data |
| `end_to_end` | Complete user journey flows            |
| `api`        | API-only tests                         |
| `smoke`      | Critical path verification             |
| `ui`         | UI-only tests                          |

---

## 📊 11. Test Data Management

### Data Sources

```text
test_data/
├── logindata.json     ← JSON format
├── logindata.csv      ← CSV format
└── logindata.xlsx     ← Excel format (primary for data-driven tests)
```

### JSON Format Example

```json
[
  { "testName": "Valid login", "email": "pavanol@abc.com", "password": "test@123", "expected": "success" },
  { "testName": "Invalid login", "email": "abcxyz@xyz.com", "password": "abcxyx", "expected": "failure" }
]
```

### Usage in Tests

```python
from utils.data_loader import read_excel_data

excel_data = read_excel_data("test_data/logindata.xlsx")

@pytest.mark.parametrize("testName,email,password,expected", excel_data)
def test_login_data_driven(page, testName, email, password, expected):
    ...
```

---

## 📋 12. Configuration Files

### 12.1 `pytest.ini`

```ini
[pytest]
testpaths = tests/ui               # Default test discovery path

addopts =
    -v                              # Verbose output
    --browser=chromium              # Default browser
    --base-url=https://tutorialsninja.com/demo/
    --video=retain-on-failure       # Record video, keep on failure
    --screenshot=only-on-failure    # Screenshot on failure
    --tracing=retain-on-failure     # Playwright trace on failure
    --html=reports/myreport.html    # HTML report path
    --alluredir=reports/allure-results
```

### 12.2 `pyproject.toml`

Defines:

- Project metadata (name, version, description)
- Runtime dependencies (11 packages)
- Dev dependencies (ruff, mypy, pre-commit)
- Ruff linter/formatter configuration
- mypy type checking configuration

### 12.3 `.pre-commit-config.yaml`

```yaml
repos:
  - repo: ruff-pre-commit     # Ruff linting + formatting
  - repo: mirrors-mypy        # Type checking (excludes tests/)
```

---

## 📈 13. Reporting

### Allure Reports

```bash
# Generate results during test run (automatic via pytest.ini)
uv run pytest --alluredir=reports/allure-results

# View interactive Allure report
allure serve reports/allure-results
```

### HTML Reports

```bash
# Generated automatically at: reports/myreport.html
# Self-contained (includes CSS/JS inline)
```

### Failure Artifacts

On test failure, the framework **automatically captures and attaches** to Allure:

| Artifact   | Format    | Condition           |
| ---------- | --------- | ------------------- |
| Screenshot | `.png`  | On test failure     |
| Video      | `.webm` | Retained on failure |
| Trace      | `.zip`  | Retained on failure |

---

## 🚀 14. CI/CD Pipeline

### GitHub Actions (`.github/workflows/playwright.yml`)

```yaml
name: Playwright Tests
on:
  push:    { branches: [main] }
  pull_request: { branches: [main] }

jobs:
  playwright:
    runs-on: ubuntu-latest
    container:
      image: mcr.microsoft.com/playwright/python:v1.55.0-noble
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-python@v6 (python 3.13)
      - uses: astral-sh/setup-uv@v5 (latest)
      - run: uv sync                           # Install dependencies
      - run: uv run ruff check .               # Lint check
      - run: uv run ruff format --check .       # Format check
      - run: xvfb-run uv run pytest             # Run tests headless
```

**Pipeline Steps:** Checkout → Python Setup → uv Install → Lint → Format → Run Tests

---

## 🔍 15. Code Quality & Linting

### Ruff Configuration

```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "B", "UP"]  # Errors, imports, bugbear, upgrades
ignore = ["E501"]                           # Line length handled by formatter
```

### Running Locally

```bash
uv run ruff check .           # Lint
uv run ruff format .          # Format
uv run mypy .                 # Type check
uv run pre-commit run --all   # Run all pre-commit hooks
```

---

## 🏃 16. How to Run Tests

### Prerequisites

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Install Playwright browsers
uv run playwright install
```

### Run Commands

```bash
# Run all UI tests (default from pytest.ini)
uv run pytest

# Run specific test file
uv run pytest tests/ui/test_login.py

# Run with headed browser (visible)
uv run pytest --headed

# Run specific browser
uv run pytest --browser=firefox
uv run pytest --browser=webkit

# Run by marker
uv run pytest -m "sanity"
uv run pytest -m "regression"
uv run pytest -m "sanity or regression"
uv run pytest -m "datadriven"

# Run in parallel
uv run pytest -n auto
uv run pytest -n 4

# Retry failed tests
uv run pytest --reruns 2 --reruns-delay 2

# Run with custom base URL
uv run pytest --base-url=https://example.com

# Run with environment selection
ENV=prod uv run pytest

# Generate Allure report
uv run pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

---

## 🔗 17. Dependency Graph

```text
conftest.py (registry)
    │
    ├── fixtures/browser.py
    │       └── uses: allure, pytest, page (from pytest-playwright)
    │
    ├── fixtures/api.py
    │       └── uses: utils/config.py (API_URL, ENV)
    │
    └── fixtures/auth.py
            └── uses: utils/constants.py (APIEndpoints)

tests/ui/test_*.py
    │
    ├── pages/*.py (inherit BasePage)
    │       └── pages/base_page.py
    │
    ├── utils/config.py (Config class)
    ├── utils/helpers.py (RandomDataUtil)
    └── utils/data_loader.py (read_excel_data, etc.)

tests/api/test_*.py  (future)
    │
    ├── api_clients/*.py (inherit BaseAPI)
    │       └── api_clients/base_api.py
    │
    └── utils/constants.py (APIEndpoints, Headers)
```

---

## 📂 18. File Reference Index

### Root Files

| File                        | Lines | Purpose                                  |
| --------------------------- | ----- | ---------------------------------------- |
| `conftest.py`             | 12    | Fixture registry — imports only         |
| `pytest.ini`              | 58    | Pytest configuration & CLI defaults      |
| `pyproject.toml`          | 57    | Project metadata & dependency management |
| `.pre-commit-config.yaml` | 13    | Pre-commit hooks configuration           |
| `.python-version`         | 1     | Python version pin (3.13)                |
| `.gitignore`              | 21    | Git ignore rules                         |

### Fixtures (`fixtures/`)

| File           | Lines | Key Exports                                             |
| -------------- | ----- | ------------------------------------------------------- |
| `browser.py` | 77    | `navigate_to_base_url`, `pytest_runtest_makereport` |
| `api.py`     | 27    | `api_context`                                         |
| `auth.py`    | 34    | `auth_token`                                          |

### Pages (`pages/`)

| File                       | Lines | Class                 | Inherits     |
| -------------------------- | ----- | --------------------- | ------------ |
| `base_page.py`           | 56    | `BasePage`          | —           |
| `home_page.py`           | 50    | `HomePage`          | `BasePage` |
| `login_page.py`          | 48    | `LoginPage`         | `BasePage` |
| `registration_page.py`   | 84    | `RegistrationPage`  | `BasePage` |
| `my_account_page.py`     | 39    | `MyAccountPage`     | `BasePage` |
| `logout_page.py`         | 31    | `LogoutPage`        | `BasePage` |
| `search_results_page.py` | 60    | `SearchResultsPage` | `BasePage` |
| `product_page.py`        | 62    | `ProductPage`       | `BasePage` |
| `shopping_cart_page.py`  | 40    | `ShoppingCartPage`  | `BasePage` |
| `checkout_page.py`       | 119   | `CheckoutPage`      | `BasePage` |

### API Clients (`api_clients/`)

| File            | Lines | Class       | Inherits |
| --------------- | ----- | ----------- | -------- |
| `base_api.py` | 48    | `BaseAPI` | —       |

### Utils (`utils/`)

| File               | Lines | Key Exports                                                      |
| ------------------ | ----- | ---------------------------------------------------------------- |
| `config.py`      | 40    | `ENV`, `BASE_URL`, `API_URL`, `Config`                   |
| `constants.py`   | 42    | `APIEndpoints`, `Headers`, `UIRoutes`                      |
| `logger.py`      | 37    | `get_logger()`                                                 |
| `data_loader.py` | 67    | `read_json_data()`, `read_csv_data()`, `read_excel_data()` |
| `helpers.py`     | 63    | `RandomDataUtil`                                               |
| `messages.py`    | 15    | UI validation constants (e.g.`WARN_PASSWORD`)                  |

### Tests (`tests/ui/`)

| File                            | Lines | Test Functions                                         | Markers            |
| ------------------------------- | ----- | ------------------------------------------------------ | ------------------ |
| `test_login.py`               | 63    | `test_invalid_user_login`, `test_valid_user_login` | regression, sanity |
| `test_login_data_driven.py`   | 35    | `test_login_data_driven`                             | datadriven         |
| `test_user_registration.py`   | 49    | `test_user_registration`                             | sanity, regression |
| `test_user_logout.py`         | 52    | `test_user_logout`                                   | regression         |
| `test_product_search.py`      | 35    | `test_product_search`                                | sanity, regression |
| `test_add_product_to_cart.py` | 43    | `test_add_product_to_cart`                           | regression         |
| `test_end_to_end.py`          | 138   | `test_end_to_end_flow`                               | end_to_end         |

---

> **Total Framework Files**: ~35 source files
> **Total Lines of Code**: ~1,500 lines (excluding tests in old Day* folders)
> **Design Level**: Senior SDET / Architect

---

## 📏 19. Strict Engineering Guidelines

To maintain the scalable design of this architect-level framework, always adhere to these rules when adding new functions or code.

### 19.1 Where to Place Common Methods (Rule of Thumb)

*If you need to import `Page` or `Locator`, it belongs in `pages/`. If it's pure standard Python logic, it belongs in `utils/`.*

| Method Type                         | Target Location               | Description & Examples                                                                                                                                                  |
| ----------------------------------- | ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Native DOM Actions**        | `pages/base_page.py`        | If the method wraps a raw Playwright command to add logging, custom waits, or error handling. Examples:`click()`, `fill()`, `wait_for()`, `is_visible()`.       |
| **Business User Flows**       | Specific POM (`pages/*.py`) | If the method navigates the user through a specific flow unique to a single piece of the website. Examples:`complete_registration()`, `login()`.                    |
| **Data Generation / Parsing** | `utils/helpers.py`          | If the method generates, formats, or calculates data and doesn't explicitly interact with the DOM via Playwright. Examples:`get_random_email()`, `generate_uuid()`. |

### 19.2 Where to Place Constants

Constants should **never** be hardcoded directly inside your test files (`test_*.py`).

1. **`utils/constants.py` ➔ Application State & Enums**: Rules of your app that rarely change. E.g. `APIEndpoints`, HTTP `Headers`, and broad groupings of static test data like `INVALID_PHONE_NUMBERS`.
2. **`utils/messages.py` ➔ UI Verification Strings**: Every string used in `expect(...).to_have_text(...)`. E.g. `WARN_PASSWORD`, `ACCOUNT_CREATED`.
3. **`utils/config.py` ➔ Environment & Credentials**: Anything reliant on external runtime flags (`qa` vs `prod`). E.g. Base URLs, admin users.
4. **`test_data/` ➔ Parameterized Test Data**: Complex iteration sets. E.g. A CSV of 50 different login combinations or edge-case users.

---
