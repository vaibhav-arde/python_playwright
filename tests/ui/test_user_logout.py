"""
Test Case: User Logout Functionality

===========================================
Test Steps
===========================================
1. Navigate to Home page → My Account → Login.
2. Log in with valid credentials.
3. Verify My Account page is displayed.
4. Click Logout.
5. Verify Logout confirmation page.
6. Click Continue and verify Home page.
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from utils.config import Config


@pytest.mark.regression
def test_user_logout(page):
    """Verify that a logged-in user can successfully log out."""

    home_page = HomePage(page)
    login_page = LoginPage(page)
    my_account_page = MyAccountPage(page)

    # Navigate to Login Page
    home_page.click_my_account()
    home_page.click_login()

    # Login with valid credentials
    login_page.set_email(Config.email)
    login_page.set_password(Config.password)
    login_page.click_login()

    # Verify My Account page
    expect(my_account_page.get_my_account_page_heading()).to_be_visible(timeout=5000)

    # Perform Logout
    logout_page = my_account_page.click_logout()

    # Verify Logout page
    expect(logout_page.get_continue_button()).to_be_visible(timeout=5000)

    # Navigate back to Home page
    logout_page.click_continue()
    expect(page).to_have_title("Your Store")
