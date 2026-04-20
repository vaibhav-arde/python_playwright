"""
Test Scenario: Logout and Immediate Re-Login Validation
"""

import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.logout_page import LogoutPage
from pages.my_account_page import MyAccountPage


@pytest.mark.ui
@pytest.mark.critical
def test_logout_and_login_immediate_same_account(authenticated_page, registered_user):
    """
    Test Scenario: Logout and Immediate Re-Login with Same Account
    Validates logging out of the application and immediately logging back in
    using the same account credentials.
    """
    page = authenticated_page

    # Prerequisite: Navigate to account page where the dropdown is visible
    base_url = page.url.split("index.php")[0]

    # Initialize Page Objects
    home_page = HomePage(page)
    my_account_page = MyAccountPage(page)
    logout_page = LogoutPage(page)
    login_page = LoginPage(page)
    
    my_account_page.open_my_account_page(base_url)

    # Step 1: Navigate to "My Account" dropdown
    my_account_page.click_my_account_dropdown()

    # Step 2: Click on "Logout" option
    my_account_page.click_logout()

    # Step 3: Verify the Logout page is displayed
    expect(logout_page.verify_logout_page_heading()).to_be_visible()

    # Step 4: Click on "Continue" button
    logout_page.click_continue()

    # Step 5: Immediately perform login again using Option A: Same account credentials
    home_page.click_my_account()
    home_page.click_login()
    
    # Login with the same registered user's credentials
    login_page.login(registered_user["email"], registered_user["password"])

    # Step 6: Verify successful login (ER-1)
    # User should be navigated to the Account page after login
    expect(my_account_page.get_my_account_page_heading()).to_be_visible()

    # "Logout" option should be visible in "My Account" dropdown after login
    my_account_page.click_my_account_dropdown()
    expect(my_account_page.verify_logout_btn_in_dropdown()).to_be_visible()


@pytest.mark.ui
@pytest.mark.critical
def test_logout_and_login_immediate_different_account(authenticated_page, dynamic_second_user):
    """
    Test Scenario: Logout and Immediate Re-Login with Different Account
    Validates logging out of the application and immediately logging back in
    using different account credentials.
    """
    page = authenticated_page

    # Prerequisite: Navigate to account page where the dropdown is visible
    base_url = page.url.split("index.php")[0]

    # Initialize Page Objects
    home_page = HomePage(page)
    my_account_page = MyAccountPage(page)
    logout_page = LogoutPage(page)
    login_page = LoginPage(page)

    my_account_page.open_my_account_page(base_url)

    # Step 1: Navigate to "My Account" dropdown
    my_account_page.click_my_account_dropdown()

    # Step 2: Click on "Logout" option
    my_account_page.click_logout()

    # Step 3: Verify the Logout page is displayed
    expect(logout_page.verify_logout_page_heading()).to_be_visible()

    # Step 4: Click on "Continue" button
    logout_page.click_continue()

    # Step 5: Immediately perform login again using Option B: Different account credentials
    home_page.click_my_account()
    home_page.click_login()
    
    # Login with dynamically generated different user's credentials
    login_page.login(dynamic_second_user["email"], dynamic_second_user["password"])

    # Step 6: Verify successful login (ER-1)
    # User should be navigated to the Account page after login
    expect(my_account_page.get_my_account_page_heading()).to_be_visible()

    # "Logout" option should be visible in "My Account" dropdown after login
    my_account_page.click_my_account_dropdown()
    expect(my_account_page.verify_logout_btn_in_dropdown()).to_be_visible()