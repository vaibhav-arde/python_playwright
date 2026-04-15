# tests/ui/test_user_login.py
# ==================================
# Validates the user login UI flow using API-driven preconditions.

from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage


def test_user_login_ui(page, registered_user):
    """Verify that a registered user can log in successfully via the UI."""
    home_page = HomePage(page)
    login_page = LoginPage(page)
    my_account_page = MyAccountPage(page)

    home_page.click_my_account()
    home_page.click_login()

    login_page.login(registered_user["email"], registered_user["password"])

    expect(my_account_page.get_my_account_page_heading()).to_be_visible(timeout=5000)
