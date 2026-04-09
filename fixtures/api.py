# fixtures/api.py
# =====================
# API-related fixtures.
# Provides an APIRequestContext for API testing.

import logging

import pytest

from utils.config import API_URL, ENV

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def api_context(playwright):
    """
    Create a Playwright APIRequestContext for the current environment.
    Session-scoped to reuse across all API tests.
    """
    base_url = API_URL.get(ENV, API_URL["qa"])
    logger.info(f"Creating API context with base URL: {base_url}")

    context = playwright.request.new_context(base_url=base_url)
    yield context
    context.dispose()
