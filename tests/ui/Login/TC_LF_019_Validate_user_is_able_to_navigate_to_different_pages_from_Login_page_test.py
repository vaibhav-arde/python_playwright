import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils import messages


@pytest.mark.ui
def test_validate_user_is_able_to_navigate_to_different_pages_from_Login_page(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    # --- Step 1: Navigate to Login Page ---
    home_page.click_my_account()
    home_page.click_login()

    login_page.click_login()

    # --- Step 2: Navigate to Register Account page ---
    login_page.click_continue_register()

    # Acceptance Criteria: User should be navigated to 'Register Account' page
    expect(page).to_have_title("Register Account")

    # --- Step 3: Navigate back to Login page ---
    page.go_back()

    # --- Step 4: Navigate to different options ---

    # A. Right Column Option: Forgotten Password
    login_page.click_forgot_password()
    expect(page).to_have_title(messages.FORGOT_PASSWORD_PAGE_TITLE)

    page.go_back()
    page.go_back()
    page.go_back()

    home_page.click_my_account()
    home_page.click_login()
    # B. Header Option: My Account Menu
    expect(page).to_have_title(messages.LOGIN_PAGE_TITLE)

    # C. Menu Option: Desktops Category
    home_page.click_desktops_category()
    home_page.click_show_all_desktops()
    expect(page).to_have_title("Desktops")

    # D. Footer Option: Contact Us
    home_page.click_contact_us()
    expect(page).to_have_title("Contact Us")
