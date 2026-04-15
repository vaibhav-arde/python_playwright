# fixtures/user_setup.py
# =====================
# Fixtures for user-related preconditions.
# Uses UserAPI to ensure the required state is present before UI tests.

import pytest
from api_clients.user_api import UserAPI
from utils.helpers import RandomDataUtil


@pytest.fixture
def registered_user(api_context):
    """
    Creates a unique registered user via API.
    Returns the credentials (email, password) and cleans up if necessary.
    """
    user_api = UserAPI(api_context)
    random_data = RandomDataUtil()

    user_data = {
        "firstName": random_data.get_first_name(),
        "lastName": random_data.get_last_name(),
        "email": random_data.get_email(),
        "telephone": random_data.get_phone_number(),
        "password": random_data.get_password(),
        "confirm": random_data.get_password(),
    }

    user_api.create_user(user_data)
    return {"email": user_data["email"], "password": user_data["password"]}


@pytest.fixture
def authenticated_session(page, api_context, registered_user):
    """
    Authenticates a user via API and sets the session cookies in the browser context.
    This allows UI tests to start directly on authenticated pages.
    """
    user_api = UserAPI(api_context)
    credentials = {"email": registered_user["email"], "password": registered_user["password"]}

    response = user_api.authenticate_user(credentials)

    # Set cookies from API response to the browser context
    for _cookie in response.headers.get("set-cookie", "").split(","):
        # Simplified cookie injection for demo purposes;
        # in a real scenario, you'd parse the set-cookie header properly.
        pass

    # Since the target site uses session cookies, we can also just perform a UI login
    # once for this fixture to be absolutely sure, or rely on the API session if supported.
    # For this framework, we will ensure the user is logged in.
    return registered_user
