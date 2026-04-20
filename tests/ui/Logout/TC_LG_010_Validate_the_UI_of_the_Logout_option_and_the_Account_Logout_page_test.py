"""
Test Scenario: Logout UI Checklist Validation
"""

import re
import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.logout_page import LogoutPage
from pages.my_account_page import MyAccountPage


@pytest.mark.ui
@pytest.mark.critical
def test_logout_ui_checklist_validation(authenticated_page):
    """
    Test Scenario: Logout UI Checklist Validation
    Validates the UI elements present in the My Account dropdown, right column,
    and the final Account Logout page.
    """
    page = authenticated_page

    # Prerequisite: Application URL is accessible and User is logged in.
    # Navigate to the Account page to see right column and My Account drop-down.
    base_url = page.url.split("index.php")[0]
    
    # Initialize Page Objects
    home_page = HomePage(page)
    my_account_page = MyAccountPage(page)
    logout_page = LogoutPage(page)

    my_account_page.open_my_account_page(base_url)

    # --- Part 1: My Account Dropdown UI Validation ---
    
    # 1. Click on "My Account" dropdown
    my_account_page.click_my_account_dropdown()

    # Verify "My Account" option inside the dropdown is present indicating proper alignment
    expect(home_page.get_my_account_inner_link()).to_be_visible()
    expect(home_page.get_my_account_inner_link()).to_be_enabled()

    # Verify "Logout" option is visible and enabled (clickable)
    expect(my_account_page.verify_logout_btn_in_dropdown()).to_be_visible()
    expect(my_account_page.verify_logout_btn_in_dropdown()).to_be_enabled()

    
    # Close the dropdown so we can interact cleanly with other elements
    my_account_page.click_my_account_dropdown()
    

    # --- Part 2: Right Column UI Validation ---
    
    # Verify "Logout" link is displayed in the right column
    expect(my_account_page.verify_logout_sidebar_visible()).to_be_visible()
    expect(my_account_page.verify_logout_sidebar_visible()).to_be_enabled()
    
    # 3. Click on "Logout" option (from the right column)
    # This clicks the sidebar link and navigates correctly to the Logout page
    my_account_page.click_logout_sidebar()
    

    # --- Part 3: 'Account Logout' Page UI Validation ---
    
    # Wait and verify navigation routed correctly
    expect(page).to_have_url(re.compile(logout_page.get_url_pattern()))

    # 4. Verify UI elements on the 'Account Logout' page
    
    # Verify Page Heading
    expect(logout_page.verify_logout_page_heading()).to_be_visible()
    
    # Verify Page Title is correct
    expect(page).to_have_title(logout_page.get_expected_title())
    
    # Verify "Continue" button is visible and clickable
    expect(logout_page.get_continue_button()).to_be_visible()
    expect(logout_page.get_continue_button()).to_be_enabled()
    
    # Verify breadcrumb is displayed correctly
    expect(logout_page.get_breadcrumb()).to_be_visible()
    expect(logout_page.get_breadcrumb()).to_contain_text("Account")
    expect(logout_page.get_breadcrumb()).to_contain_text("Logout")
    
    # Verify layout consistency (header, footer, right column present)
    expect(logout_page.get_header()).to_be_visible()
    expect(logout_page.get_footer()).to_be_visible()
    expect(logout_page.get_right_column()).to_be_visible()