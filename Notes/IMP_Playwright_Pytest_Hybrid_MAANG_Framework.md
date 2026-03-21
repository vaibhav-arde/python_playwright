
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

