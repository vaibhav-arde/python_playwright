
---
---

# Pytest HTML reports

Here are **clear notes** you can keep for reference or training on **Generating PyTest HTML Reports with Dynamic Report Name** (works well with **uv + pytest-html**).

---

# PyTest HTML Report with Dynamic Report Name

## 1. Install Required Plugin

PyTest itself does not generate HTML reports. We use the **pytest-html plugin**.
If using **uv package manager**:
```bash
uv add pytest-html
```
If dev dependency:
```bash
uv add --dev pytest-html
```

---

# 2. Basic HTML Report Generation

Run tests with:
```bash
uv run pytest --html=report.html
```

Example output:

```
project
│
├─ tests
│   └─ test_sample.py
│
└─ report.html
```

Open `report.html` in a browser to see results.

---

# 3. Recommended Command (Self-contained Report)

```bash
uv run pytest --html=reports/report.html --self-contained-html
```
Why `--self-contained-html`?
- embeds CSS and JS inside report
- easier to share
- no external dependencies

---

# 4. Configure HTML Report in pytest.ini

Create **pytest.ini**

```ini
[pytest]
addopts = --html=reports/report.html --self-contained-html
testpaths = tests
```
Now simply run:

```bash
uv run pytest
```

---

# 5. Problem with Static Report Name

Using pytest.ini:
```
report.html
```

Every run **overwrites previous report**.
Example:
```
report.html
report.html
report.html
```

This is not ideal for automation frameworks.

---

# 6. Dynamic Report Name Solution

`pytest.ini` does **not support dynamic values** like timestamps.
We solve it using **conftest.py**.

---

# 7. Dynamic HTML Report Name using conftest.py

Create **conftest.py**

```python
import os
from datetime import datetime

def pytest_configure(config):
    
    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    config.option.htmlpath = f"reports/report_{timestamp}.html"
```

---

# 8. Run Tests

```
uv run pytest
```
Output:
```
reports/
    report_2026-03-13_10-42-11.html
```
Every execution generates a **new report**.

Example:

```
report_2026-03-13_10-40.html
report_2026-03-13_11-15.html
report_2026-03-13_12-30.html
```

---

# 9. Recommended Project Structure

```
project
│
├─ tests
│   ├─ test_login.py
│   └─ test_cart.py
│
├─ reports
│
├─ conftest.py
├─ pytest.ini
└─ pyproject.toml
```

---

# 10. Adding Metadata to HTML Report

You can show **environment info** inside the report.
Add to **conftest.py**
```python
def pytest_configure(config):
    
    config._metadata["Project"] = "Playwright Automation"
    config._metadata["Tester"] = "Vaibhav Arde"
    config._metadata["Environment"] = "QA"
```
Report will display:

```
Project: Playwright Automation
Tester: Vaibhav Arde
Environment: QA
```

---

# 11. Example Output Summary

HTML report shows:
```
Total Tests : 10
Passed      : 8
Failed      : 1
Skipped     : 1
Duration    : 20s
```

You can also see:

- logs
- test duration
- failure trace
- screenshots (if configured)

---

# 12. Industry Best Practice

Most automation frameworks generate reports like:

```
reports/
   report_chrome_20260313_1045.html
   report_firefox_20260313_1045.html
```

Often combined with:

- browser name
- environment
- build number

Example:

```
report_staging_chrome_20260313_1045.html
```

---

# 13. Useful pytest-html Options

|Option|Purpose|
|---|---|
|`--html=report.html`|generate report|
|`--self-contained-html`|embed CSS/JS|
|`--css=style.css`|custom styling|
|`--title="Test Report"`|report title|

Example:
```
pytest --html=report.html --self-contained-html --title="Automation Test Report"
```

---

# 14. Key Takeaways

✔ pytest-html plugin is required  
✔ pytest.ini supports only static configuration  
✔ dynamic report name requires **conftest.py**  
✔ timestamp prevents report overwrite  
✔ reports should be stored inside **reports folder**

---
---

# Pytest Allure reports

Your notes are already good 👍. I **polished them for clarity, structure, and training/documentation use**. I fixed formatting, explanations, and code blocks so you can **share them with a team or use them in training**.

---

# Allure Test Report in Playwright using PyTest

## Overview

**Allure Report** is a powerful and visually rich reporting tool used with automation frameworks like **PyTest**.

It provides an **interactive dashboard** with detailed information about test execution.

The report can include:
- Test execution status (Pass / Fail / Skip)
- Step-by-step execution details
- Screenshots and attachments
- Logs and stack traces
- Execution timeline
- Test history and statistics

Because of these capabilities, **Allure is widely used in modern SDET automation frameworks**.

---

# Step 1: Install Allure PyTest Plugin

Install the Allure PyTest integration plugin.

```bash
pip install allure-pytest
```

If you are using **uv package manager**, run:

```bash
uv add --dev allure-pytest
```

---

# Step 2: Install Allure Command Line Tool

The **Allure CLI (Command Line Interface)** is required to generate and view reports.

---

## Windows Installation
1. Go to  
    [https://github.com/allure-framework/allure2/releases](https://github.com/allure-framework/allure2/releases)
2. Download the latest **.zip** file.
3. Extract the archive.
4. Add the **bin directory** to your **System PATH**.

Example:

```
C:\allure-2.xx.x\bin
```

Verify installation:

```bash
allure --version
```

---

## macOS Installation

Using **Homebrew**:

```bash
brew install allure
```

---

## Linux Installation

Using **Snap**:

```bash
sudo snap install allure --classic
```

Verify installation:

```bash
allure --version
```

---

# Step 3: Configure Allure in pytest.ini

Add the following configuration to **pytest.ini**.

```ini
[pytest]
addopts = --alluredir=reports/allure-results
```

### Explanation

|Option|Description|
|---|---|
|`--alluredir`|Specifies where PyTest stores Allure test result files|
|`reports/allure-results`|Folder containing raw JSON test results|

These results will later be converted into a **visual HTML report**.

---

# Step 4: Attach Screenshots on Test Failures

To capture screenshots when a test fails, update **conftest.py**.

```python
from pathlib import Path
import pytest
from slugify import slugify
import allure


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    pytest_html = item.config.pluginmanager.getplugin("html")

    outcome = yield
    report = outcome.get_result()

    extra = getattr(report, "extra", [])
    screen_file = ""

    if report.when == "call":

        xfail = hasattr(report, "wasxfail")

        if (report.failed or xfail) and "page" in item.funcargs:

            page = item.funcargs["page"]

            screenshot_dir = Path("screenshots")
            screenshot_dir.mkdir(exist_ok=True)

            screen_file = str(
                screenshot_dir / f"{slugify(item.nodeid)}.png"
            )

            page.screenshot(path=screen_file)

            # Add screenshot to HTML report
            if (report.skipped and xfail) or (report.failed and not xfail):

                extra.append(pytest_html.extras.png(screen_file))

                # Attach screenshot to Allure report
                allure.attach.file(
                    screen_file,
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )

                report.extra = extra
```

### What this code does

When a test fails:
1. A screenshot is captured using Playwright
2. The screenshot is saved in the **screenshots folder**
3. The screenshot is attached to the **Allure report**
4. The screenshot can also appear in the **HTML report (if used)**

---

# Step 5: Create and Run Your Tests

Create Playwright tests as usual.

Example test file:

```python
from playwright.sync_api import Page, expect


def test_google_search(page: Page):

    page.goto("https://www.google.com")

    expect(page).to_have_title("Google")


def test_bing_search(page: Page):

    page.goto("https://www.bing.com")

    # Intentionally incorrect to demonstrate failure
    expect(page).to_have_title("Bing123")
```

Run the tests:

```bash
pytest
```

After execution, PyTest generates a results folder:

```
reports/allure-results
```

This folder contains raw **JSON result files** used by Allure.

---

# Step 6: Generate and View the Allure Report

There are two ways to view the report.

---

# Option 1: Temporary Report

Generate and open report automatically:

```bash
allure serve reports/allure-results
```

What happens:
1. Allure generates the report
2. Starts a temporary server
3. Opens the report in your browser

⚠ The report is **not saved permanently**.

---

# Option 2: Permanent Report

Generate a report that can be saved and shared.

```bash
allure generate reports/allure-results -o reports/allure-report --clean
```

Open the report:

```bash
allure open reports/allure-report
```

Now the report is stored inside:

```
reports/allure-report
```

---

# Example Project Structure

```
project
│
├── tests
│    ├── test_google.py
│
├── reports
│    ├── allure-results
│    └── allure-report
│
├── screenshots
│
├── conftest.py
├── pytest.ini
└── pyproject.toml
```

---

# Combining Multiple Report Formats

You can generate multiple reports in a single test run.

Example:

```bash
pytest \
--html=reports/report.html \
--junitxml=reports/results.xml \
--alluredir=reports/allure-results
```

This generates:

|Report|Purpose|
|---|---|
|HTML Report|Quick local debugging|
|JUnit XML|CI/CD pipelines|
|Allure Report|Detailed interactive report|

---

# Summary

Allure reporting workflow:

```
Run Tests
   ↓
Generate allure-results
   ↓
Convert results to HTML report
   ↓
View interactive report
```

Commands:

```
pytest
allure serve reports/allure-results
```

---

# Why Teams Prefer Allure

Compared to basic HTML reports, Allure provides:
- Interactive dashboards
- Step-level reporting
- Attachments (screenshots, logs, videos)
- Execution timeline
- Rich debugging information

Because of these features, **Allure is commonly used in enterprise automation frameworks**.

---
---

