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
from utils import change_password_constants


@pytest.mark.ui
def test_valid_user_login(page, registered_user):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    my_account_page = MyAccountPage(page)

    home_page.click_my_account()
    home_page.click_login()

    login_page.login(
        registered_user[change_password_constants.EMAIL_TXT],
        registered_user[change_password_constants.PASSWORD_FIELD_TYPE],
    )

    expect(my_account_page.get_my_account_page_heading()).to_be_visible()
