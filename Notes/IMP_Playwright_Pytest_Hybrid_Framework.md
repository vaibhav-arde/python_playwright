Below is a **complete, industry-standard Playwright + Pytest framework** that incorporates **everything we discussed**:

* UI + API support
* Modular fixtures (via `conftest.py`)
* BasePage + BaseAPI
* Centralized constants/endpoints
* Auth handling
* Reporting (Allure + HTML)
* CI/CD
* Scalability & best practices

This is **Senior SDET / Architect level** 👇

---

# 🏗️ 1️⃣ Final Enterprise Framework Structure

```text
project/
│
├── tests/
│   ├── ui/
│   │   ├── test_login.py
│   │   └── test_dashboard.py
│   │
│   ├── api/
│   │   ├── test_booking.py
│   │   └── test_user.py
│
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   ├── dashboard_page.py
│   └── components/              # optional (advanced)
│       ├── header_component.py
│
├── api_clients/
│   ├── base_api.py
│   ├── booking_api.py
│   └── user_api.py
│
├── fixtures/
│   ├── browser.py
│   ├── api.py
│   └── auth.py
│
├── utils/
│   ├── config.py
│   ├── constants.py
│   ├── logger.py
│   ├── data_loader.py
│   └── helpers.py
│
├── test_data/
│   └── test_data.json
│
├── reports/
│   ├── allure-results/
│   ├── allure-report/
│   └── html/
│
├── .github/workflows/
│   └── ci.yml
│
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

---

# 🧠 2️⃣ Core Design Principles

```text
✔ Separation of concerns
✔ No hardcoding (use constants/config)
✔ Reusable fixtures
✔ Page Object Model (UI)
✔ API Client abstraction (API)
✔ Centralized authentication
✔ Scalable & CI/CD ready
```

---

# 🧩 3️⃣ Constants (Endpoints, Headers)

```python
# utils/constants.py

class APIEndpoints:
    BASE = "/api/v1"
    LOGIN = f"{BASE}/auth/login"
    BOOKING = f"{BASE}/booking"
    USERS = f"{BASE}/users"


class Headers:
    JSON = {
        "Content-Type": "application/json"
    }
```

✅ No hardcoding in tests

---

# ⚙️ 4️⃣ Config (Environment Handling)

```python
# utils/config.py

import os

ENV = os.getenv("ENV", "qa")

BASE_URL = {
    "qa": "https://qa.app.com",
    "prod": "https://app.com"
}

API_URL = {
    "qa": "https://qa.api.com",
    "prod": "https://api.com"
}
```

---

# 🧱 5️⃣ Base Page (UI Layer)

```python
# pages/base_page.py

class BasePage:

    def __init__(self, page):
        self.page = page

    def open(self, url):
        self.page.goto(url)

    def click(self, locator):
        self.page.locator(locator).click()

    def fill(self, locator, value):
        self.page.locator(locator).fill(value)

    def get_text(self, locator):
        return self.page.locator(locator).inner_text()

    def is_visible(self, locator):
        return self.page.locator(locator).is_visible()
```

---

# 📄 Example Page Object

```python
# pages/login_page.py

from pages.base_page import BasePage

class LoginPage(BasePage):

    def login(self, username, password):
        self.fill("#username", username)
        self.fill("#password", password)
        self.click("#login")
```

---

# 🌐 6️⃣ Base API (API Layer)

```python
# api_clients/base_api.py

class BaseAPI:

    def __init__(self, request, headers=None):
        self.request = request
        self.headers = headers or {}

    def get(self, endpoint, **kwargs):
        return self.request.get(endpoint, headers=self.headers, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.request.post(endpoint, headers=self.headers, **kwargs)

    def put(self, endpoint, **kwargs):
        return self.request.put(endpoint, headers=self.headers, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.request.delete(endpoint, headers=self.headers, **kwargs)
```

---

# 📦 API Client Example

```python
# api_clients/booking_api.py

from api_clients.base_api import BaseAPI
from utils.constants import APIEndpoints

class BookingAPI(BaseAPI):

    def create_booking(self, payload):
        return self.post(APIEndpoints.BOOKING, data=payload)

    def get_booking(self, booking_id):
        return self.get(f"{APIEndpoints.BOOKING}/{booking_id}")
```

---

# 🔐 7️⃣ Fixtures Strategy (Correct Industry Approach)

---

## fixtures/api.py

```python
import pytest
from utils.config import API_URL, ENV

@pytest.fixture
def api_context(playwright):
    return playwright.request.new_context(
        base_url=API_URL[ENV]
    )
```

---

## fixtures/browser.py

```python
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        yield page
        browser.close()
```

---

## fixtures/auth.py

```python
import pytest
from utils.constants import APIEndpoints

@pytest.fixture(scope="session")
def auth_token(api_context):

    res = api_context.post(APIEndpoints.LOGIN, data={
        "username": "admin",
        "password": "password"
    })

    return res.json()["token"]
```

---

## 🔗 conftest.py (ONLY registry)

```python
from fixtures.api import *
from fixtures.browser import *
from fixtures.auth import *
```

---

# 🧪 8️⃣ UI Test Example

```python
def test_login(page):

    page.goto("https://app.com")

    login = LoginPage(page)
    login.login("admin", "password")

    assert "dashboard" in page.url
```

---

# 🔗 9️⃣ API Test Example

```python
def test_booking(api_context):

    api = BookingAPI(api_context)

    res = api.create_booking({"firstname": "John"})
    booking_id = res.json()["bookingid"]

    res2 = api.get_booking(booking_id)

    assert res2.status == 200
```

---

# 🔥 🔟 Hybrid Test (UI + API)

```python
def test_api_ui_flow(api_context, page):

    api = BookingAPI(api_context)

    res = api.create_booking({"firstname": "John"})
    booking_id = res.json()["bookingid"]

    page.goto(f"https://app.com/booking/{booking_id}")

    assert page.locator("text=John").is_visible()
```

---

# 📊 1️⃣1️⃣ Reporting

---

## Allure (Recommended)

```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

---

## HTML Report

```bash
pytest --html=reports/html/report.html
```

---

## Screenshot Hook

```python
# conftest.py

import pytest

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.failed:
        page = item.funcargs.get("page", None)
        if page:
            page.screenshot(path="reports/failure.png")
```

---

# 🚀 1️⃣2️⃣ CI/CD (GitHub Actions)

```yaml
name: Run Tests

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-python@v4

      - run: pip install -r requirements.txt

      - run: playwright install

      - run: pytest --alluredir=reports/allure-results
```

---

# ⚡ 1️⃣3️⃣ Advanced Additions

---

## Parallel Execution

```bash
pytest -n auto
```

---

## Retry Failed Tests

```bash
pytest --reruns 2
```

---

## Markers

```ini
[pytest]
markers =
    ui
    api
    smoke
    regression
```

---

# 🧠 1️⃣4️⃣ Key Architecture Decisions (From Our Discussion)

---

## ✔ Constants

```text
Centralized → maintainable → no duplication
```

---

## ✔ Base Classes

```text
BasePage → UI reuse
BaseAPI → API reuse
```

---

## ✔ Fixtures

```text
fixtures/ → logic
conftest.py → registry only
```

---

## ✔ Hybrid Testing

```text
API creates data → UI validates → fast + reliable
```

---

# 🎯 Final Interview Answer (Strongest Version)

> I designed a scalable Playwright + Pytest hybrid framework supporting both UI and API automation. It follows Page Object Model for UI and a dedicated API client layer. Fixtures are modularized and registered via conftest.py. I centralized API endpoints using constants, implemented BasePage and BaseAPI for reusability, and integrated Allure reporting and CI/CD pipelines. The framework supports parallel execution, environment configuration, and hybrid testing flows.

---

# 💡 Final Takeaway

```text
Junior → Writes tests
Mid → Uses POM
Senior → Designs framework with:
         ✔ API layer
         ✔ fixtures architecture
         ✔ constants/config
         ✔ CI/CD + reporting
```

---
---

Perfect—let’s **upgrade your current Playwright + Pytest framework to MAANG-level** step by step.
We’ll add the **3 missing layers**:

```text
1. DSL (Domain Specific Layer)  → Business readable tests
2. Data Factory                → Dynamic test data
3. Test Context                → Shared state across steps
```

This is exactly what differentiates **good vs elite frameworks**.

---

# 🧠 FINAL TARGET ARCHITECTURE (MAANG-STYLE)

```text
tests  → uses → DSL (App Layer)
DSL    → uses → API Clients + Pages
Data   → provided by → Factories
State  → managed by → TestContext
```

---

# 🚀 STEP 1️⃣ Add DSL Layer (App Layer)

👉 This is the **biggest upgrade**

---

## 📁 New Folder

```text
app/
  ├── app.py
```

---

## Example: app/app.py

```python
class App:

    def __init__(self, page, api_context):
        self.page = page
        self.api_context = api_context

    # UI Action
    def login(self, user):
        self.page.goto("/login")
        self.page.fill("#username", user["username"])
        self.page.fill("#password", user["password"])
        self.page.click("#login")

    # API Action
    def create_booking(self, data):
        res = self.api_context.post("/booking", data=data)
        return res.json()

    # UI Validation
    def verify_booking(self, booking_id):
        self.page.goto(f"/booking/{booking_id}")
        return self.page.locator("text=Booking Confirmed").is_visible()
```

---

## ✅ Test BEFORE (your current)

```python
def test_booking(api_context, page):
    res = api_context.post("/booking", data={})
    booking_id = res.json()["bookingid"]

    page.goto(f"/booking/{booking_id}")
    assert page.locator("text=Booking Confirmed").is_visible()
```

---

## ✅ Test AFTER (MAANG style)

```python
def test_booking_flow(app, user_factory):

    user = user_factory.create_user()

    app.login(user)

    booking = app.create_booking({"firstname": "John"})

    assert app.verify_booking(booking["bookingid"])
```

👉 Cleaner, readable, business-focused

---

# 🧪 STEP 2️⃣ Add Data Factory

👉 No hardcoded test data anymore

---

## 📁 New Folder

```text
factories/
  ├── user_factory.py
  ├── booking_factory.py
```

---

## Example: factories/user_factory.py

```python
import random

class UserFactory:

    def create_user(self):
        return {
            "username": f"user{random.randint(1000,9999)}",
            "password": "password123"
        }
```

---

## Example: factories/booking_factory.py

```python
import random

class BookingFactory:

    def create_booking(self):
        return {
            "firstname": f"John{random.randint(1,100)}",
            "lastname": "Doe"
        }
```

---

## Fixture for factory

```python
@pytest.fixture
def user_factory():
    return UserFactory()
```

---

# 🧠 STEP 3️⃣ Add Test Context (Shared State)

👉 Very powerful for complex workflows

---

## 📁 New File

```text
utils/
  ├── test_context.py
```

---

## Example: test_context.py

```python
class TestContext:

    def __init__(self):
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)
```

---

## Fixture

```python
@pytest.fixture
def context():
    return TestContext()
```

---

## Usage

```python
def test_flow(app, context):

    booking = app.create_booking({"firstname": "John"})

    context.set("booking_id", booking["bookingid"])

    assert app.verify_booking(context.get("booking_id"))
```

---

# 🔗 STEP 4️⃣ Add App Fixture

```python
@pytest.fixture
def app(page, api_context):
    return App(page, api_context)
```

---

# 🧩 FINAL STRUCTURE (UPGRADED)

```text
project/
│
├── tests/
│
├── app/                    ✅ DSL Layer
│   └── app.py
│
├── factories/              ✅ Data Factory
│   ├── user_factory.py
│   └── booking_factory.py
│
├── pages/
├── api_clients/
├── fixtures/
├── utils/
│   ├── test_context.py     ✅ Context
│
├── conftest.py
```

---

# 🔥 FINAL MAANG-STYLE TEST

```python
def test_complete_flow(app, user_factory, booking_factory, context):

    user = user_factory.create_user()
    booking_data = booking_factory.create_booking()

    app.login(user)

    booking = app.create_booking(booking_data)

    context.set("booking_id", booking["bookingid"])

    assert app.verify_booking(context.get("booking_id"))
```

---

# 🧠 WHY THIS IS POWERFUL

---

## DSL Layer

```text
Tests read like business flow
```

---

## Factory

```text
No hardcoded data
Reusable + scalable
```

---

## Context

```text
Share data across steps cleanly
```

---

# 🎯 INTERVIEW GOLD ANSWER

If asked:

**“How would you design a scalable automation framework?”**

Answer:

> I design frameworks with a DSL layer for business-readable tests, a data factory layer for dynamic test data, and a shared test context for managing state. This approach improves readability, maintainability, and scalability, and aligns with how large-scale systems like MAANG companies structure their automation frameworks.

---

# 💡 FINAL TRANSFORMATION

```text
Before → Test scripts
After  → Test platform
```

---
---

