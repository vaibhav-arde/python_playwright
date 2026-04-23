# fixtures/auth.py
# =====================
# Thin authentication fixtures.
# Auth bootstrap/setup lives in setup/setuptest.py.

import logging

import pytest

from setup.setuptest import DEFAULT_BASE_URL, ensure_auth_state_silently
from utils.constants import APIEndpoints

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def authenticated_page(new_context, auth_state_path, request, launch_browser):
    """
    Return a Playwright page initialized with the saved auth state.
    Tests using this fixture start with a logged-in session.
    """
    base_url = request.config.getoption("--base-url", default=DEFAULT_BASE_URL) or DEFAULT_BASE_URL

    context = new_context(storage_state=auth_state_path)
    page = context.new_page()
    page.goto(base_url)

    try:
        yield page
    finally:
        try:
            context.close()
        except ValueError:
            pass
        ensure_auth_state_silently(launch_browser, base_url)


@pytest.fixture(scope="session")
def auth_token(api_context):
    """
    Obtain an authentication token via API login.
    Session-scoped so authentication happens only once per test run.
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
