# setup/setuptest.py
# =====================
# Auth setup/bootstrap helpers and fixtures.
# Handles generated user creation, registration, logout, login,
# and persistent storage state setup for authenticated UI tests.

import json
import logging
from pathlib import Path

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.logout_page import LogoutPage
from pages.registration_page import RegistrationPage
from utils import messages
from utils.constants import FilePaths
from utils.config import BASE_URL, ENV
from utils.user_registration import generate_user_data
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = BASE_URL.get(ENV, BASE_URL["qa"])


def build_url(base_url: str, path: str = "") -> str:
    """Safely join base URL and path (cross-platform safe for URLs)."""
    return urljoin(base_url.rstrip("/") + "/", path)


def _save_registered_user(user_data: dict) -> None:
    """Persist the registered user so expired sessions can log in again."""
    FilePaths.SESSION_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    FilePaths.AUTH_USER_PATH.write_text(json.dumps(user_data, indent=2), encoding="utf-8")
    logger.info("Saved registered user data to %s", FilePaths.AUTH_USER_PATH)


def load_registered_user() -> dict | None:
    """Load the previously registered user details, if available."""
    if not FilePaths.AUTH_USER_PATH.exists():
        return None

    try:
        user_data = json.loads(FilePaths.AUTH_USER_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        logger.warning("Could not read saved user data from %s: %s", FilePaths.AUTH_USER_PATH, exc)
        return None

    required_keys = {"firstName", "lastName", "email", "telephone", "password"}
    if not required_keys.issubset(user_data):
        logger.warning("Saved user data is incomplete. Expected keys: %s", sorted(required_keys))
        return None

    return user_data


def _is_session_valid(browser, base_url: str) -> bool:
    """Check whether the saved auth state still opens the My Account page."""
    if not FilePaths.AUTH_STATE_PATH.exists():
        return False

    context = browser.new_context(storage_state=str(FilePaths.AUTH_STATE_PATH), base_url=base_url)
    page = context.new_page()

    try:
        page.goto(build_url(base_url))
        heading = page.locator(f'h2:has-text("{messages.MY_ACCOUNT_HEADING}")')
        heading.wait_for(timeout=5000)
        return heading.is_visible()
    except Exception as exc:
        logger.info("Saved auth state is no longer valid: %s", exc)
        return False
    finally:
        context.close()


def _save_storage_state(context) -> None:
    """Persist the current browser storage state to auth_state.json."""
    FilePaths.SESSION_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=str(FilePaths.AUTH_STATE_PATH))
    logger.info("Saved auth state to %s", FilePaths.AUTH_STATE_PATH)


def _login_and_save_state(browser, base_url: str, user_data: dict) -> None:
    """Log in with an existing registered user and save the storage state."""
    context = browser.new_context(base_url=base_url)
    page = context.new_page()

    try:
        logger.info("Logging in with saved registered user: %s", user_data["email"])
        page.goto(build_url(base_url))

        home_page = HomePage(page)
        login_page = LoginPage(page)

        home_page.click_my_account()
        home_page.click_login()
        login_page.login(user_data["email"], user_data["password"])

        expect(page.locator(f'h2:has-text("{messages.MY_ACCOUNT_HEADING}")')).to_be_visible(
            timeout=10000
        )
        _save_storage_state(context)
    finally:
        context.close()


def _register_login_and_save_state(browser, base_url: str) -> None:
    """
    Register a new random user, log out of the auto-login session,
    log back in with the same credentials, and persist auth state.
    """
    context = browser.new_context(base_url=base_url)
    page = context.new_page()

    try:
        user_data = generate_user_data()
        logger.info("No saved user found. Registering a new user: %s", user_data["email"])
        page.goto(build_url(base_url))

        home_page = HomePage(page)
        registration_page = RegistrationPage(page)
        logout_page = LogoutPage(page)
        login_page = LoginPage(page)

        home_page.click_my_account()
        home_page.click_register()
        confirmation_msg = registration_page.complete_registration(user_data)
        expect(confirmation_msg).to_have_text(messages.ACCOUNT_CREATED, timeout=10000)

        registration_page.click_continue()
        expect(page.locator(f'h2:has-text("{messages.MY_ACCOUNT_HEADING}")')).to_be_visible(
            timeout=10000
        )

        home_page.click_my_account()
        logout_page.logout()

        home_page.click_my_account()
        home_page.click_login()
        login_page.login(user_data["email"], user_data["password"])
        expect(page.locator(f'h2:has-text("{messages.MY_ACCOUNT_HEADING}")')).to_be_visible(
            timeout=10000
        )

        _save_registered_user(user_data)
        _save_storage_state(context)
    finally:
        context.close()


def _ensure_auth_state(browser, base_url: str) -> None:
    """Make sure a valid auth_state.json exists before tests use it."""
    if _is_session_valid(browser, base_url):
        logger.info("Reusing existing auth state from %s", FilePaths.AUTH_STATE_PATH)
        return

    user_data = load_registered_user()
    if user_data:
        logger.info("Auth state missing or expired. Recreating it with saved credentials.")
        _login_and_save_state(browser, base_url, user_data)
        return

    logger.info("No auth state or saved user found. Creating a new registered session.")
    _register_login_and_save_state(browser, base_url)


def ensure_auth_state_silently(launch_browser, base_url: str) -> None:
    """Refresh auth state in a temporary headless browser so no extra UI pops up."""
    temp_browser = launch_browser(headless=True)
    try:
        _ensure_auth_state(temp_browser, base_url)
    finally:
        temp_browser.close()



def get_auth_state_path(launch_browser, base_url: str) -> str:
    FilePaths.SESSION_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    ensure_auth_state_silently(launch_browser, base_url)
    return str(FilePaths.AUTH_STATE_PATH)

def get_registered_user() -> dict:
    user_data = load_registered_user()
    if user_data is None:
        raise RuntimeError("Registered user data was not created after auth setup.")
    return user_data
