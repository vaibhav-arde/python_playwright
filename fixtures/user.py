# fixtures/user.py
# =====================
# User-related fixtures.

import pytest
from playwright.sync_api import expect
from setup.setuptest import DEFAULT_BASE_URL
from utils.user_registration import generate_user_data
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage


@pytest.fixture(scope="session")
def dynamic_second_user(launch_browser, request):
    """
    Dynamically register a second user in a hidden browser context
    to be used as valid 'different account' credentials.
    """
    base_url = request.config.getoption("--base-url", default=DEFAULT_BASE_URL) or DEFAULT_BASE_URL
    user_data = generate_user_data()

    temp_browser = launch_browser(headless=True)
    context = temp_browser.new_context(base_url=base_url)
    page = context.new_page()

    try:
        page.goto(base_url)
        home_page = HomePage(page)
        reg_page = RegistrationPage(page)

        # Register the user
        home_page.click_my_account()
        home_page.click_register()
        confirmation_msg = reg_page.complete_registration(user_data)
        expect(confirmation_msg).to_be_visible(timeout=10000)
    finally:
        context.close()
        temp_browser.close()

    return user_data
