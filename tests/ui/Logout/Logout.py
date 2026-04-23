"""
Test Case: User Logout Functionality

===========================================
Test Steps
===========================================
1. Start with an authenticated session (login is skipped via session storage).
2. Verify My Account page is displayed.
3. Click Logout.
4. Verify Logout confirmation page.
5. Click Continue and verify Home page.
"""

import pytest
from playwright.sync_api import expect

from pages.my_account_page import MyAccountPage


@pytest.mark.regression
def test_user_logout(authenticated_page):
    """Verify that a logged-in user can successfully log out.

    Uses the authenticated_page fixture to skip the UI login flow.
    The session storage is loaded from auth_state.json, so the user
    is already logged in when the test starts.
    """
    page = authenticated_page

    # Navigate to My Account page
    page.goto(page.url.split("index.php")[0] + "index.php?route=account/account")

    my_account_page = MyAccountPage(page)

    # Verify My Account page is loaded with session
    expect(my_account_page.get_my_account_page_heading()).to_be_visible(timeout=5000)

    # Perform Logout
    logout_page = my_account_page.click_logout()

    # Verify Logout page
    expect(logout_page.get_continue_button()).to_be_visible(timeout=5000)

    # Navigate back to Home page
    logout_page.click_continue()
    expect(page).to_have_title("Your Store")
