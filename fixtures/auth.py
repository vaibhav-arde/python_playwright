# fixtures/auth.py
# =====================
# Thin authentication fixtures.
# Only pytest fixtures live here.
# All logic is delegated to setup/setuptest.py

import logging
import pytest

from setup.setuptest import (
    DEFAULT_BASE_URL,
    ensure_auth_state_silently,
    get_auth_state_path,
    get_registered_user,
)
from utils.constants import APIEndpoints

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def auth_state_path(launch_browser, request):
    """
    Provides a valid auth state file path.
    Ensures login/registration is done before tests.
    """
    base_url = request.config.getoption("--base-url", default=DEFAULT_BASE_URL) or DEFAULT_BASE_URL
    return get_auth_state_path(launch_browser, base_url)


@pytest.fixture(scope="function")
def authenticated_page(new_context, auth_state_path, request, launch_browser):
    """
    Returns a Playwright page already logged in using storage state.
    """
    base_url = request.config.getoption("--base-url", default=DEFAULT_BASE_URL) or DEFAULT_BASE_URL

    context = new_context(storage_state=auth_state_path)
    page = context.new_page()
    page.goto(base_url)

    try:
        yield page
    finally:
        context.close()
        # Refresh auth state silently after test
        ensure_auth_state_silently(launch_browser, base_url)


@pytest.fixture(scope="session")
def registered_user(auth_state_path):
    """
    Returns stored registered user.
    Depends on auth_state_path to ensure user exists.
    """
    return get_registered_user()


@pytest.fixture(scope="session")
def auth_token(api_context):
    """
    API-based authentication token (session scoped).
    """
    logger.info("Authenticating via API to obtain session token")

    res = api_context.post(
        APIEndpoints.LOGIN,
        data={
            "username": "admin",
            "password": "password",
        },
    )

    token = res.json().get("token", "")
    logger.info("Authentication token obtained successfully")
    return token
