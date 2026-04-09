# fixtures/auth.py
# =====================
# Authentication fixtures.
# Provides session-scoped auth token for authenticated API calls.

import logging

import pytest

from utils.constants import APIEndpoints

logger = logging.getLogger(__name__)


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
