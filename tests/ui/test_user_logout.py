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

from pages.my_account_page import MyAccountPage


@pytest.mark.regression
def test_user_logout(authenticated_page):
    """Verify that a logged-in user can successfully log out."""
    page = authenticated_page
    my_account_page = MyAccountPage(page)

    # Verify My Account page (already logged in via fixture)
    expect(my_account_page.get_my_account_page_heading()).to_be_visible(timeout=5000)

    # Perform Logout
    logout_page = my_account_page.click_logout()

    # Verify Logout page
    expect(logout_page.get_continue_button()).to_be_visible(timeout=5000)

    # Navigate back to Home page
    logout_page.click_continue()
    expect(page).to_have_title("Your Store")
