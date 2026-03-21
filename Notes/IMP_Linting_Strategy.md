# Modern Linting & Quality Strategy

This document outlines the **production-grade linting, formatting, and type-checking strategy** implemented in our Playwright + Pytest test automation framework. This strategy is specifically optimized for speed, reliability, and modern tooling via `uv`.

---

## 🚀 1. Core Tooling Stack

Our setup entirely replaces older, slower legacy Python linting stacks (like `flake8` + `black` + `isort`) with a faster, unified toolchain.

| Purpose | Tool | Why We Use It |
| :--- | :--- | :--- |
| **Package Management** | `uv` | Industry-leading speed, replaces `pip`/`venv`, handles lockfiles deterministically. |
| **Linting & Formatting** | `Ruff` | Written in Rust, it does the exact same job as Flake8 + Black + Isort in ~10 milliseconds. |
| **Static Type Checking** | `Mypy` | Prevents hidden bugs by enforcing proper Python type hints (e.g., `str \| None`). |
| **Git Automation** | `pre-commit` | Automatically blocks bad code from even entering the repository during `git commit`. |

---

## ⚙️ 2. Configuration & Structure

The framework is configured centrally to avoid scattering linting files.

### Single Source of Truth (`pyproject.toml`)
All of our rules live inside `pyproject.toml`.

**Ruff Configuration:**
* **Line Length:** 100 characters.
* **Target Version:** Python 3.12/3.13.
* **Rules Enforced:** 
  * `E` (Style errors)
  * `F` (Logical Pyflakes errors - like unused imports)
  * `W` (Warnings)
  * `I` (Import sorting)
  * `B` (Bugbear - catches common Python pitfalls)
  * `UP` (Forces modern Python upgrade syntax)
* **Testing Exceptions:** The assert statement rule (`S101`) is specifically ignored inside the `tests/*` folder.

**Mypy Configuration:**
* Strict typing targeted at Python `3.12`.
* Missing external typing stubs are ignored globally (`ignore_missing_imports = true`).
* The `tests/` directory is excluded from strict type validation to focus Mypy purely on the framework structure (`pages/`, `utilities/`, etc).

### Pre-commit Configuration (`.pre-commit-config.yaml`)
Pre-commit is configured to call exactly three isolated actions:
1. `ruff` (The base linter)
2. `ruff-format` (The auto-formatter)
3. `mypy` (The type-checker)

---

## ⚡ 3. Developer Workflow

As an automation engineer on this project, the workflow is entirely automated.

### 1. While Writing Code (Local Checks)
If you want to validate or format your code *before* you are ready to commit, you can use `uv` directly:
```bash
# Check for Pyflakes errors and auto-fix the safe ones
uv run ruff check . --fix

# Auto-format all Python files to the team standard
uv run ruff format .
```

### 2. When Committing Code (Git Hooks)
You do not need to remember to run the linters. When you type:
```bash
git add .
git commit -m "feat: added new checkout tests"
```
The **Pre-commit** hook will automatically pause the commit, run Ruff, run Mypy, and run the formatter. 
* ✅ If the code is perfect, the commit proceeds instantly.
* 🛠️ If Ruff finds a formatting issue, it will auto-fix the issue and fail the hook (`git commit` is blocked). Simply review the changes, re-stage them (`git add .`), and commit again!
* ❌ If Mypy finds a strict type error, you must fix it manually.

---

## 🌐 4. CI/CD Enforcement (GitHub Actions)

Local pre-commit hooks can be bypassed by developers using `git commit --no-verify`. Therefore, the linting standards are permanently enforced at the CI/CD pipeline level.

Inside `.github/workflows/playwright.yml`:
```yaml
      - name: Lint Code
        run: |
          uv run ruff check .
          uv run ruff format --check .
```
This runs exactly the same version of Ruff as the developers run locally. If this step fails in the GitHub Action, **the Pull Request is permanently blocked** and the `pytest` suite will not even waste time executing.
