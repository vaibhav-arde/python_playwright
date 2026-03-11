In Playwright, the **testing framework** refers to the **architecture/pattern used to organize tests, reusable components, and test logic**. Playwright itself provides tools, but the **framework structure is designed by the automation engineer**.

Below are the **most common testing framework types used with Playwright** (important for SDET interviews and real projects).

---

# 1️⃣ Linear (Record-and-Playback) Framework

This is the **simplest form** of automation.

### Structure

Tests are written in a **straight sequence of steps** without abstraction.

Example:

```javascript
test('login test', async ({ page }) => {
  await page.goto('https://example.com');
  await page.fill('#username', 'admin');
  await page.fill('#password', 'admin123');
  await page.click('#login');
});
```

### Characteristics

✔ Very easy to write
✔ Good for quick demos
❌ Not scalable
❌ Lots of code duplication

Used mostly for:

* Small projects
* POCs
* Learning Playwright

---

# 2️⃣ Modular Testing Framework

The application is divided into **modules (components)** and each module has reusable functions.

### Example structure

```
tests/
modules/
   login.js
   cart.js
```

Example:

```javascript
async function login(page) {
  await page.fill('#username', 'admin');
  await page.fill('#password', 'admin123');
  await page.click('#login');
}
```

Then tests call the module.

✔ Reusable components
✔ Less duplication
❌ Still tightly coupled with test data

---

# 3️⃣ Data-Driven Framework

Test data is separated from test logic.

Test data can come from:

```
JSON
CSV
Excel
API
Database
```

Example JSON:

```
testdata.json
```

```json
{
  "username": "admin",
  "password": "admin123"
}
```

Test example:

```javascript
const data = require('./testdata.json');

test('login test', async ({ page }) => {
  await page.fill('#username', data.username);
  await page.fill('#password', data.password);
});
```

✔ Multiple data sets
✔ Reusable tests
✔ Better coverage

---

# 4️⃣ Keyword-Driven Framework

Test actions are defined as **keywords**, and tests are built using them.

Example keywords:

```
OPEN_BROWSER
LOGIN
ADD_ITEM
LOGOUT
```

Implementation:

```javascript
async function LOGIN(page, user, pass) {
  await page.fill('#username', user);
  await page.fill('#password', pass);
  await page.click('#login');
}
```

Test case example:

```
OPEN_BROWSER
LOGIN admin admin123
VERIFY_DASHBOARD
```

✔ Non-technical testers can understand
✔ Very structured
❌ Requires heavy framework development

---

# 5️⃣ Page Object Model (POM) Framework ⭐ (Most Common)

Each page of the application becomes a **class or module**.

### Example structure

```
pages/
   loginPage.js
tests/
   login.spec.js
```

Login Page Object:

```javascript
class LoginPage {
  constructor(page) {
    this.page = page;
    this.username = '#username';
    this.password = '#password';
  }

  async login(user, pass) {
    await this.page.fill(this.username, user);
    await this.page.fill(this.password, pass);
    await this.page.click('#login');
  }
}
```

Test:

```javascript
test('login', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.login('admin','admin123');
});
```

✔ Most widely used
✔ Maintainable
✔ Reusable
✔ Clean code

---

# 6️⃣ Hybrid Framework ⭐⭐ (Most Used in Industry)

Combination of multiple frameworks:

```
Page Object Model
+
Data Driven
+
Fixtures
+
Utilities
```

Typical Playwright framework structure:

```
tests/
pages/
fixtures/
utils/
test-data/
config/
```

Example:

```
tests
pages
fixtures
utils
data
```

Benefits:

✔ Highly scalable
✔ Clean architecture
✔ Industry standard

---

# 7️⃣ BDD Framework (Behavior Driven Development)

Playwright can integrate with BDD tools like:

* Cucumber
* Playwright BDD

Test written in **Gherkin syntax**.

Example:

```
Feature: Login

Scenario: Valid login
  Given user opens login page
  When user enters username and password
  Then user should see dashboard
```

Step definition:

```javascript
Given('user opens login page', async ({ page }) => {
  await page.goto('/login');
});
```

✔ Business readable
✔ Collaboration with product owners
❌ More setup

---

# 📊 Summary Table

| Framework         | Difficulty | Usage                  |
| ----------------- | ---------- | ---------------------- |
| Linear            | Easy       | Learning               |
| Modular           | Medium     | Small projects         |
| Data Driven       | Medium     | Data testing           |
| Keyword Driven    | Hard       | Enterprise frameworks  |
| Page Object Model | Medium     | Most common            |
| Hybrid            | Advanced   | Industry standard      |
| BDD               | Medium     | Business collaboration |

---

# ⭐ Recommended for Playwright (Real Industry)

Most companies use:

```
Hybrid Framework
     |
     |-- Page Object Model
     |-- Fixtures
     |-- Data Driven
     |-- Utilities
```

---
---
