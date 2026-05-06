import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage


@pytest.mark.ui
def test_validate_the_ui_of_the_login_page(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    # --- Step 1: Navigate to Login Page ---
    home_page.click_my_account()
    home_page.click_login()

    expect(login_page.get_email_field()).to_be_visible()
    expect(login_page.get_password_field()).to_be_visible()
    expect(login_page.get_login_button()).to_be_visible()
    expect(login_page.get_forgot_password()).to_be_visible()
