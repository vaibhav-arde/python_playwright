# fixtures/auth.py
# =====================
# Authentication fixtures.
# Provides session-scoped auth state for authenticated UI and API calls.
# Session storage is PERSISTENT — registration and login happen only once.
# Subsequent test runs reuse the saved auth_state.json and user_data.json.

import json
import logging
from pathlib import Path

import pytest

from utils.config import API_URL, ENV
from utils.constants import APIEndpoints
from utils.user_registration import generate_user_data, register_user
from pages.logout_page import LogoutPage
from pages.home_page import HomePage
from pages.login_page import LoginPage

logger = logging.getLogger(__name__)

BASE_URL = "https://tutorialsninja.com/demo/"
SESSION_STORAGE_DIR = Path("test_data")
AUTH_STATE_PATH = SESSION_STORAGE_DIR / "auth_state.json"
USER_DATA_PATH = SESSION_STORAGE_DIR / "user_data.json"


def _saved_session_exists() -> bool:
    """Check if both auth state and user data files exist on disk."""
    return AUTH_STATE_PATH.exists() and USER_DATA_PATH.exists()


def _load_user_data() -> dict:
    """Load previously saved user credentials from disk."""
    with open(USER_DATA_PATH, "r") as f:
        return json.load(f)


def _save_user_data(user_data: dict) -> None:
    """Save user credentials to disk for reuse across test runs."""
    with open(USER_DATA_PATH, "w") as f:
        json.dump(user_data, f, indent=2)


def _is_session_valid(browser) -> bool:
    """
    Verify the saved session is still valid by loading it and
    navigating to the My Account page. If it redirects to login,
    the session has expired.
    """
    try:
        context = browser.new_context(
            storage_state=str(AUTH_STATE_PATH),
            base_url=BASE_URL,
        )
        page = context.new_page()
        page.goto(f"{BASE_URL}index.php?route=account/account")

        # If we land on the account page, session is valid
        heading = page.locator('h2:has-text("My Account")')
        heading.wait_for(timeout=5000)
        is_valid = heading.is_visible()
        context.close()
        return is_valid
    except Exception:
        return False


def _perform_registration_and_login(browser) -> dict:
    """
    Full flow: generate user → register → logout → login → save state.
    Called only when no valid saved session exists.
    """
    context = browser.new_context(base_url=BASE_URL)
    page = context.new_page()

    logger.info("No saved session found — performing registration and login")
    page.goto(BASE_URL)

    # 1. Generate user data
    user_data = generate_user_data()

    # 2. Register via UI
    register_user(page, user_data)

    # 3. Logout
    logout_page = LogoutPage(page)
    page.goto(f"{BASE_URL}index.php?route=account/logout")
    logout_page.click_continue()

    # 4. Login with the generated credentials
    home_page = HomePage(page)
    home_page.click_my_account()
    home_page.click_login()

    login_page = LoginPage(page)
    login_page.login(user_data["email"], user_data["password"])

    # Wait for account page to confirm login success
    page.locator('h2:has-text("My Account")').wait_for()

    # 5. Save session state and user credentials to disk
    context.storage_state(path=str(AUTH_STATE_PATH))
    _save_user_data(user_data)
    logger.info(f"Saved auth state to {AUTH_STATE_PATH}")
    logger.info(f"Saved user data to {USER_DATA_PATH}")

    context.close()
    return user_data


@pytest.fixture(scope="session")
def registered_user(browser):
    """
    Provide user credentials for an authenticated session.

    - If auth_state.json and user_data.json already exist AND the session
      is still valid → reuse them (NO registration, NO login).
    - Otherwise → perform the full registration + login flow and save
      the results for future runs.
    """
    SESSION_STORAGE_DIR.mkdir(parents=True, exist_ok=True)

    if _saved_session_exists():
        logger.info("Found saved session files — validating session...")
        if _is_session_valid(browser):
            logger.info("Saved session is VALID — skipping registration and login")
            return _load_user_data()
        else:
            logger.info("Saved session is EXPIRED — re-registering")

    return _perform_registration_and_login(browser)


@pytest.fixture(scope="session")
def auth_state_path(registered_user):
    """Returns the path to the saved auth state JSON file."""
    return str(AUTH_STATE_PATH)


@pytest.fixture(scope="function")
def authenticated_page(browser, auth_state_path, request):
    """
    Returns a Playwright Page initialized with the saved auth state.
    Tests using this fixture will skip the UI login flow.
    """
    base_url = request.config.getoption("--base-url", default=BASE_URL)

    context = browser.new_context(storage_state=auth_state_path, base_url=base_url)
    page = context.new_page()
    page.goto(base_url)

    yield page
    context.close()


# Keep existing API token if needed for API tests
@pytest.fixture(scope="session")
def auth_token(api_context):
    """
    Obtain an authentication token via API login.
    Session-scoped so authentication happens only once per test run.
    """
    logger.info("Authenticating via API to obtain session token")

    res = api_context.post(
        APIEndpoints.LOGIN,
        data={            "username": "admin",
            "password": "password",
        },
    )

    token = res.json().get("token", "")
    logger.info("Authentication token obtained successfully")
    return token
