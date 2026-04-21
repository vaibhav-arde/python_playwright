import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils import messages
from utils.config import Config


@pytest.mark.ui
def test_validate_logging_into_the_Application_using_inactive_credentials(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    # 1. Reach the Login Page via My Account dropdown
    home_page.click_my_account()
    home_page.click_login()

    # 2. Login with valid credentials from fixture
    login_page.login(Config.inactive_email, Config.inactive_password)

    # Assert redirection to the Account Login page, proving the session is inactive
    expect(page).to_have_title(messages.LOGIN_PAGE_TITLE)
