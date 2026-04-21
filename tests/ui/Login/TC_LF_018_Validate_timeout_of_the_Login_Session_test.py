import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.config import Config
from utils.constants import UIRoutes


@pytest.mark.critical
@pytest.mark.ui
def test_validate_timeout_of_the_login_session(context):
    # Close default tabs to avoid empty pages in headed mode
    pages = context.pages
    for p in pages:
        p.close()

    page = context.new_page()
    home_page = HomePage(page)
    login_page = LoginPage(page)

    # 1. Click on 'My Account' Dropmenu
    page.goto(UIRoutes.BASE_URL)
    home_page.click_my_account()

    # 2. Click on 'Login' option
    home_page.click_login()

    # 3. Enter valid email address and password from Config
    # Note: Test requirements specified pavanoltraining@gmail.com / 12345
    # but requested use of config file.
    login_page.login(Config.email, Config.password)

    # 4. Simulate session timeout using Cookie Manipulation
    # We clear the cookies to simulate a session that has expired/been lost
    context.clear_cookies()

    page.reload()

    # 5. Perform any action on the Application to trigger session check
    home_page.click_my_account()

    # 6. Acceptance Criteria: User should be automatically logged out.
    # Since the application does not show a literal "session expired" message,
    # we verify the user is logged out by checking that the Logout link is no longer visible.
    expect(home_page.logout_link()).not_to_be_visible()
