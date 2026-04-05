"""
Test Case: User Login Functionality

===========================================
Test Steps
===========================================

Test Case 1: Verify Login with Invalid Credentials
--------------------------------------------------
1. Navigate to the Home page.
2. Click on "My Account" → "Login".
3. Enter invalid email and password.
4. Click Login.
5. Verify error message is displayed.

Test Case 2: Verify Login with Valid Credentials
------------------------------------------------
1. Navigate to the Home page.
2. Click on "My Account" → "Login".
3. Enter valid email and password.
4. Click Login.
5. Verify "My Account" page heading is visible.
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from utils.config import Config


@pytest.mark.regression
def test_invalid_user_login(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    home_page.click_my_account()
    home_page.click_login()

    login_page.set_email(Config.invalid_email)
    login_page.set_password(Config.invalid_password)
    login_page.click_login()

    expect(login_page.get_login_error()).to_be_visible(timeout=5000)


@pytest.mark.sanity
def test_valid_user_login(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    my_account_page = MyAccountPage(page)

    home_page.click_my_account()
    home_page.click_login()

    login_page.set_email(Config.email)
    login_page.set_password(Config.password)
    login_page.click_login()

    expect(my_account_page.get_my_account_page_heading()).to_be_visible(timeout=5000)
