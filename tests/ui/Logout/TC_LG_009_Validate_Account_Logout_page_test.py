"""
Test Scenario: Logout Page UI and Navigation Validation
"""

import re
import pytest
from playwright.sync_api import expect
from pages.logout_page import LogoutPage
from pages.my_account_page import MyAccountPage


@pytest.mark.ui
@pytest.mark.critical
def test_validate_account_logout_page_ui(authenticated_page):
    """
    Test Scenario: Logout Page UI and Navigation Validation
    Validates various UI elements (heading, title, URL, breadcrumbs) 
    of the Account Logout page after a user logs out.
    """
    page = authenticated_page

    # Prerequisite: Navigate to account page where the 'My Account' dropdown is available
    base_url = page.url.split("index.php")[0]
    
    # Initialize Page Objects
    my_account_page = MyAccountPage(page)
    logout_page = LogoutPage(page)

    my_account_page.open_my_account_page(base_url)

    # Step 1: Navigate to "My Account" dropdown
    my_account_page.click_my_account_dropdown()

    # Step 2: Click on "Logout" option
    my_account_page.click_logout()

    # Validation (ER-1)
    # ------------------
    # 1. Verify correct Page Heading is displayed
    expect(logout_page.verify_logout_page_heading()).to_be_visible()

    # 2. Verify correct Page Title is displayed
    expect(page).to_have_title(logout_page.get_expected_title())

    # 3. Verify correct Page URL contains the logout route
    expect(page).to_have_url(re.compile(logout_page.get_url_pattern()))

    # 4. Verify Breadcrumb is displayed correctly
    breadcrumb = logout_page.get_breadcrumb()
    expect(breadcrumb).to_be_visible()
    
    # Asserting that the breadcrumb correctly contains the key navigational steps.
    expect(breadcrumb).to_contain_text("Account")
    expect(breadcrumb).to_contain_text("Logout")