# 🚀 Playwright Python Automation - The Ultimate Master Guide

This master document contains the complete, consolidated knowledge from all training notes, PDFs, and implementation strategies in this workspace.

---

## 📑 Table of Contents
1. [Environment Setup & Installation](#1-environment-setup--installation)
2. [Pytest Masterclass (Fundamentals to Advanced)](#2-pytest-masterclass)
3. [Playwright Essentials (Debugging & Evidence)](#3-playwright-essentials)
4. [Data-Driven Testing (DDT)](#4-data-driven-testing-ddt)
5. [Page Object Model (POM) & Design Patterns](#5-page-object-model-pom--design-patterns)
6. [API Testing & Authentication](#6-api-testing--authentication)
7. [Framework Engineering (Hybrid & MAANG-Level)](#7-framework-engineering)
8. [CI/CD (Jenkins & GitHub Actions)](#8-cicd-jenkins--github-actions)
9. [Shadow DOM & Modern Web Challenges](#9-shadow-dom--modern-web-challenges)
10. [AI in Automation (LLM, Agents, MCP)](#10-ai-in-automation)

---

# 1. Environment Setup & Installation

### 📦 Package Manager: `uv` (Recommended)
`uv` is a high-performance Python package manager that replaces `pip` and `venv`.

```powershell
# Install uv on Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Initialize Project
uv init playwright-project
cd playwright-project
uv venv
uv add playwright pytest pytest-playwright
playwright install  # Installs Chromium, Firefox, WebKit
```

### 🛠️ Required Plugins for Frameworks
- `pytest-xdist`: Parallel execution.
- `pytest-html`: HTML reports.
- `allure-pytest`: Advanced reporting.
- `pytest-rerunfailures`: Flaky test handling.
- `openpyxl`: Excel support.
- `Faker`: Random data generation.
- `python-slugify`: Filename-safe strings.

---

# 2. Pytest Masterclass

### 📏 Naming Conventions
Pytest uses discovery rules to find tests.
- **Files**: `test_*.py` or `*_test.py`
- **Functions**: `test_*`
- **Classes**: `Test*` (Do not use `__init__`)
- **Methods in Classes**: `test_*`

### 💻 Running Tests (CLI)
- `pytest`: Run all.
- `pytest -v` / `-vv`: Verbose output.
- `pytest -s`: Show print statements.
- `pytest -k "login"`: Filter by name.
- `pytest -m smoke`: Run by marker.
- `pytest -n auto`: Run in parallel.
- `pytest --maxfail=2`: Stop after N failures.
- `pytest --reruns 2`: Retry failed tests.

### 🔬 Fixtures (The Powerhouse)
Fixtures handle setup and teardown.

**Scopes:**
1. `function`: Every test.
2. `class`: Once per class.
3. `module`: Once per file.
4. `session`: Once per suite (e.g., Auth, DB).

**Teardown Example:**
```python
@pytest.fixture
def db_conn():
    conn = connect()
    yield conn  # Test runs here
    conn.close() # Teardown
```

**Advanced Fixtures:**
- `autouse=True`: Runs without being requested.
- `usefixtures`: `@pytest.mark.usefixtures("fix_name")` for side-effects.
- `conftest.py`: Shared directory-level configuration.

---

# 3. Playwright Essentials

### 📸 Screenshots
- `page.screenshot(path='...')`
- `full_page=True`: Entire scrollable area.
- `element.screenshot(...)`: Specific component.

### 🎥 Video & Tracing
**pytest.ini configuration:**
```ini
[pytest]
addopts = --video=retain-on-failure --tracing=retain-on-failure
```
- **Trace Viewer**: Provides a "DVR" of the test (Network, DOM, Console).
  - Open with: `playwright show-trace trace.zip`

---

# 4. Data-Driven Testing (DDT)

| Source | Library | Use Case |
| :--- | :--- | :--- |
| **Hardcoded** | N/A | Quick POCs. |
| **JSON** | `json` | Structured/Nested data. |
| **CSV** | `csv` | Simple tables, manual edits. |
| **Excel** | `openpyxl` | Complex enterprise data. |

### 📊 Excel Implementation
```python
from openpyxl import load_workbook
import pytest

def get_excel_data():
    wb = load_workbook("data.xlsx")
    sheet = wb.active
    return [tuple(row) for row in sheet.iter_rows(min_row=2, values_only=True)]

@pytest.mark.parametrize("user, pwd, expected", get_excel_data())
def test_login(page, user, pwd, expected):
    ...
```

---

# 5. Page Object Model (POM) & Design Patterns

### 🏗️ Core Concept
Separate **UI Locators** and **Actions** from **Test Logic**.
- **Page Class**: One class per web page.
- **Variables**: Store locators.
- **Methods**: Store user actions (login, logout, search).

### 🌟 Advanced Patterns
1. **BasePage Pattern**: Shared parent class with common methods (`click`, `fill`, `wait`).
2. **Component Object Model**: Dedicated classes for UI widgets (Navbar, Footer, SearchCards).
3. **Page Factory Style**: Centralized locator dictionaries or constants inside the class.

---

# 6. API Testing & Authentication

### 🌐 HTTP Methods
- `GET`: Retrieve data.
- `POST`: Create data.
- `PUT`: Update data.
- `DELETE`: Remove data.
- `PATCH`: Partial update.

### 🔐 Authentication Types
1. **Basic Auth**: `http_credentials={'user': '...', 'pass': '...'}`.
2. **Bearer Token (JWT)**: `extra_http_headers={'Authorization': 'Bearer <token>'}`.
3. **API Key**: `headers={'x-api-key': '...'}` or query params.
4. **OAuth 2.0**: Fetch token first via POST, then use as Bearer.

---

# 7. Framework Engineering

### 🏗️ Hybrid Architecture
- **API Creates Data** → **UI Validates**.
- Fast, stable, and reduces UI flake.

### 💎 MAANG-Level Upgrades (The 3 Missing Layers)
1. **DSL (Domain Specific Layer)**: An `App` class that provides business methods (`app.purchase_item(sku)`).
2. **Data Factory**: Classes to generate dynamic data using `Faker`.
3. **Test Context**: A shared object to pass state (e.g., `order_id`) across complex workflow steps.

---

# 8. CI/CD (Jenkins & GitHub Actions)

### 🚀 GitHub Actions (`playwright.yml`)
Runs on push/pull request. Uses the official Playwright Docker container.
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    container: mcr.microsoft.com/playwright/python:v1.55.0-noble
    steps:
      - uses: actions/checkout@v5
      - run: uv sync
      - run: uv run pytest
```

### 👷 Jenkins Setup
1. **Pre-req**: JDK installed.
2. **Run**: `java -jar jenkins.war`.
3. **Plugins**: Allure, Git, Pipeline.
4. **Pipeline**: Checkout → Env Setup → Install → Run → Publish Allure.

---

# 9. Shadow DOM & Modern Web Challenges

### 🌑 What is Shadow DOM?
Isolated HTML/CSS inside a component (encapsulation).
- **Open**: Testable via `shadowRoot`.
- **Closed**: Hard to automate (isolated).

### ✅ Playwright Handling
Playwright **automatically** pierces Open Shadow DOM. No special syntax is usually needed.
- `page.locator('button')` will find buttons inside shadow roots by default!

---

# 10. AI in Automation

### 🤖 Terminology
- **LLM (Large Language Model)**: The "Brain" (ChatGPT, Gemini). Generates code but doesn't execute.
- **Agent**: An AI system that uses tools to perform real-world actions (e.g., Running tests).
- **MCP (Model Context Protocol)**: The "Bridge" connecting LLMs to external tools (Browsers, DBs).

### 🎭 Playwright MCP
Allows LLMs to control browsers directly, understanding the page via the **Accessibility Tree** rather than just images.

---
*Generated by Antigravity AI Assistant - All Rights Reserved*
