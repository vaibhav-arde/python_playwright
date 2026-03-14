Below are **polished, structured notes for Page Object Model (POM) in Playwright using PyTest**, based on your PDF content and improved for **training, interview preparation, and documentation**.

---

# Page Object Model (POM) in Playwright (PyTest)

## Overview

**Page Object Model (POM)** is a **design pattern used in test automation** to create **maintainable, reusable, and readable test code**.

The main idea of POM is to **separate test logic from UI interactions**.

Instead of writing locators and UI actions directly in test files, they are placed inside **page classes**.

According to the notes in the uploaded material, POM organizes automation code so that **each page is represented as a class, elements are variables, and actions are methods**. 

---

# Key Concepts of Page Object Model

In POM:

### 1. Page = Class

Each web page of the application is represented as a **class**.

Example:

```python
class LoginPage:
```

---

### 2. Elements = Variables

UI elements are stored as **locators inside class variables**.

Example:

```python
self.username = page.locator("#username")
```

---

### 3. Actions = Methods

Operations performed on elements are written as **methods**.

Example:

```python
def login(self, username, password):
```

---

# Why Use Page Object Model

POM provides several advantages for automation frameworks.

### Code Reusability

Page methods can be reused across multiple test cases.

Example:

```python
login_page.login()
```

instead of repeating locator logic in every test.

---

### Easy Maintenance

If the UI changes, only the **page class needs to be updated**.

Example:

If locator changes:

```python
# Old
page.locator("#username")

# New
page.locator("#user_name")
```

You update **one file only**.

---

### Better Readability

Test files become easier to understand because they focus only on **test steps**.

Example:

Without POM:

```python
page.locator("#username").fill("admin")
page.locator("#password").fill("admin123")
page.locator("#login").click()
```

With POM:

```python
login_page.login("admin", "admin123")
```

---

### Scalability

POM is ideal for **large projects with many pages and test cases**.

Example structure:

```
tests
pages
utils
fixtures
```

This keeps automation frameworks organized.

---

# Problem Without POM

If POM is not used:

1. **Locator duplication**
2. **High maintenance**
3. **Low readability**

For example:

```
test1 → locator1
test2 → locator1
test3 → locator1
```

If the locator changes, **all test files must be updated**.

The diagram in the uploaded notes illustrates that **multiple tests depend on page classes**, which centralize UI logic. 

---

# Example: Page Object Class

Example page class (`search_page.py`).

```python
class SearchPage:

    def __init__(self, page):
        self.page = page

        self.search_input = page.locator(
            '[aria-label="Enter your search term"]'
        )

    def navigate(self):
        self.page.goto("https://bing.com")

    def search(self, text):
        self.search_input.fill(text)
        self.search_input.press("Enter")
```

This class contains:

| Component      | Purpose                      |
| -------------- | ---------------------------- |
| `__init__()`   | initialize page and locators |
| `search_input` | locator                      |
| `navigate()`   | page action                  |
| `search()`     | user action                  |

---

# Example Test Using Page Object

Test file: `test_search.py`

```python
from search_page import SearchPage


def test_search(browser):

    page = browser.new_page()

    search_page = SearchPage(page)

    search_page.navigate()

    search_page.search("Playwright automation")
```

Now the test file contains only **business logic**.

---

# Recommended Framework Structure

A clean Playwright + PyTest framework using POM:

```
project
│
├── tests
│   ├── test_login.py
│   └── test_search.py
│
├── pages
│   ├── login_page.py
│   └── search_page.py
│
├── utils
│
├── conftest.py
│
├── pytest.ini
│
└── playwright.config.py
```

---

# Best Practices for POM in Playwright

### 1. Keep Locators Inside Page Classes

Bad:

```
test_login.py
page.locator()
```

Good:

```
login_page.py
self.login_button
```

---

### 2. Avoid Assertions in Page Classes

Page classes should contain **actions**, not test validations.

Bad:

```python
assert page.title() == "Home"
```

Better:

Assertions should stay inside test files.

---

### 3. Use Meaningful Method Names

Bad:

```python
click1()
fill1()
```

Good:

```python
login()
search_product()
add_to_cart()
```

---

### 4. Group Page Elements and Actions

Example:

```
LoginPage
 ├ elements
 ├ actions
```

---

# Example Real Page Object (Login Page)

```python
class LoginPage:

    def __init__(self, page):

        self.page = page

        self.username = page.locator("#username")

        self.password = page.locator("#password")

        self.login_button = page.locator("#login")

    def navigate(self):

        self.page.goto("https://example.com/login")

    def login(self, username, password):

        self.username.fill(username)

        self.password.fill(password)

        self.login_button.click()
```

---

# Test Using This Page

```python
def test_valid_login(page):

    login_page = LoginPage(page)

    login_page.navigate()

    login_page.login("admin", "admin123")
```

---

# Summary

Page Object Model improves automation frameworks by:

* separating UI logic from tests
* improving maintainability
* enabling code reuse
* improving readability
* supporting scalable frameworks

Workflow:

```
Test
 ↓
Page Object
 ↓
UI Elements
```

Tests interact with **page methods**, and page methods interact with **UI elements**.

---
---

These three patterns are **advanced design approaches used on top of Page Object Model (POM)** to make automation frameworks **cleaner, reusable, and scalable**—especially in **large Playwright + PyTest frameworks**.

I’ll explain them in a **simple, interview-ready way** with examples.

---

# 1. BasePage Pattern

## Concept

A **BasePage** is a **parent class** that contains common methods used across multiple pages.

Instead of repeating the same actions in every page class, you **inherit them from BasePage**.

Common methods usually include:

* click
* fill
* wait
* navigation
* assertions
* logging

---

## Problem Without BasePage

Example:

```python
class LoginPage:

    def click_login(self):
        self.page.locator("#login").click()
```

```python
class SearchPage:

    def click_search(self):
        self.page.locator("#search").click()
```

Every page repeats **same actions**.

---

## Solution with BasePage

### BasePage

```python
class BasePage:

    def __init__(self, page):
        self.page = page

    def click(self, locator):
        locator.click()

    def fill(self, locator, value):
        locator.fill(value)

    def navigate(self, url):
        self.page.goto(url)
```

---

### LoginPage

```python
class LoginPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self.username = page.locator("#username")
        self.password = page.locator("#password")
        self.login_btn = page.locator("#login")

    def login(self, user, pwd):

        self.fill(self.username, user)
        self.fill(self.password, pwd)
        self.click(self.login_btn)
```

---

## Benefits

✔ Avoid duplicate code
✔ Centralized common logic
✔ Easier maintenance

---

# 2. Component Object Model

## Concept

Sometimes **web pages contain reusable components** like:

* navigation bars
* headers
* footers
* product cards
* search widgets

Instead of placing these elements in page classes, we create **component classes**.

This is called **Component Object Model**.

---

## Example Website

Example page structure:

```
Home Page
 ├ Navbar
 ├ Product List
 ├ Footer
```

Instead of putting everything in **HomePage**, we create separate components.

---

## Navbar Component

```python
class Navbar:

    def __init__(self, page):

        self.page = page

        self.login_link = page.locator("#login")
        self.cart_link = page.locator("#cart")

    def go_to_login(self):

        self.login_link.click()

    def go_to_cart(self):

        self.cart_link.click()
```

---

## HomePage

```python
class HomePage:

    def __init__(self, page):

        self.page = page

        self.navbar = Navbar(page)

    def open(self):

        self.page.goto("https://example.com")
```

---

## Test Example

```python
def test_navigation(page):

    home = HomePage(page)

    home.open()

    home.navbar.go_to_login()
```

---

## Benefits

✔ Reusable components
✔ Smaller page classes
✔ Cleaner framework architecture

---

# 3. Page Factory Style Locators

## Concept

In traditional POM, locators are written directly.

Example:

```python
self.username = page.locator("#username")
```

In **Page Factory pattern**, locators are defined in a **centralized way**, and methods use them dynamically.

This pattern improves **maintainability and readability**.

---

## Example Without Page Factory

```python
class LoginPage:

    def __init__(self, page):

        self.page = page
        self.username = page.locator("#username")
        self.password = page.locator("#password")
```

---

## Example With Page Factory Style

```python
class LoginPage:

    USERNAME = "#username"
    PASSWORD = "#password"
    LOGIN_BTN = "#login"

    def __init__(self, page):

        self.page = page

    def login(self, user, pwd):

        self.page.locator(self.USERNAME).fill(user)
        self.page.locator(self.PASSWORD).fill(pwd)
        self.page.locator(self.LOGIN_BTN).click()
```

---

## Another Advanced Example

Using locator dictionary.

```python
LOCATORS = {
    "username": "#username",
    "password": "#password",
    "login_btn": "#login"
}
```

Then:

```python
self.page.locator(LOCATORS["username"])
```

---

## Benefits

✔ Centralized locator management
✔ Easy updates if UI changes
✔ Cleaner code

---

# Comparison of All Three Patterns

| Pattern         | Purpose                         |
| --------------- | ------------------------------- |
| BasePage        | shared actions                  |
| Component Model | reusable UI components          |
| Page Factory    | centralized locator definitions |

---

# Real Enterprise Framework Structure

Large Playwright frameworks usually look like:

```
automation-framework
│
├── pages
│   ├ login_page.py
│   ├ search_page.py
│
├── components
│   ├ navbar.py
│   ├ product_card.py
│
├── core
│   ├ base_page.py
│
├── tests
│   ├ test_login.py
│
├── utils
│
└── fixtures
```

---

# How They Work Together

```
Tests
   ↓
Page Objects
   ↓
Components
   ↓
BasePage Utilities
```

---

# Interview Explanation (Short Version)

If asked in an interview:

**BasePage pattern**

> A parent class containing reusable methods like click, fill, navigation used by all page classes.

**Component Object Model**

> Represents reusable UI parts like headers, navbars, or product cards as separate classes.

**Page Factory pattern**

> Centralized locator management where selectors are defined as constants or dictionaries and used by page methods.

---
---