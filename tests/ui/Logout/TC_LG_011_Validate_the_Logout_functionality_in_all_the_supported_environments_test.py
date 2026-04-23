"""
Test Scenario: Logout Functionality Across Supported Environments
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.logout_page import LogoutPage
from pages.my_account_page import MyAccountPage


@pytest.mark.ui
@pytest.mark.critical
def test_logout_supported_environments(authenticated_page):
    """
    Test Scenario: Logout Functionality Across Supported Environments
    Validates that a logged-in user can successfully log out of the application.
    This test is parameterized to explicitly execute sequentially across
    Chromium, Firefox, and WebKit to ensure cross-environment stability.
    """
    page = authenticated_page

    # Prerequisite: Application URL is accessible and User is logged in.
    # Navigate to the Account page directly to begin standard flow
    base_url = page.url.split("index.php")[0]

    # Initialize Page Objects
    home_page = HomePage(page)
    my_account_page = MyAccountPage(page)
    logout_page = LogoutPage(page)

    my_account_page.open_my_account_page(base_url)

    # Step 1: Click on "My Account" dropdown
    my_account_page.click_my_account_dropdown()

    # Step 2: Select "Logout" option
    my_account_page.click_logout()

    # Step 3: Verify logout is successful (ER-1)

    # Validation 1: User should be navigated to the 'Account Logout' page
    expect(page).to_have_title(logout_page.get_expected_title())

    # Validation 2: Logout page heading should be correct
    expect(logout_page.verify_logout_page_heading()).to_be_visible()

    # Validation 3: "Continue" button should be visible and clickable
    expect(logout_page.get_continue_button()).to_be_visible()
    expect(logout_page.get_continue_button()).to_be_enabled()

    # Step 4: After clicking "Continue", user should be redirected to the Home page
    logout_page.click_continue()

    # Native OpenCart default Home Page title mapping
    expect(page).to_have_title(home_page.get_title())

    # Validation 5: "Login" option should be visible within My Account options
    home_page.click_my_account()
    expect(home_page.verify_login_btn_visible()).to_be_visible()

    # Validation 6: "Logout" option should not be visible anymore
    expect(home_page.verify_logout_btn()).not_to_be_visible()
