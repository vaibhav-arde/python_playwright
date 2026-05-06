import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from utils import messages


@pytest.mark.ui
def test_validate_the_different_ways_of_navigating_to_the_Login_page(page):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)
    login_page = LoginPage(page)

    # --- Step 1: Navigate to Login Page ---
    home_page.click_my_account()
    home_page.click_register()

    registration_page.click_login_page_link()
    expect(page).to_have_title(messages.LOGIN_PAGE_TITLE)

    login_page.click_right_column_login()
    expect(page).to_have_title(messages.LOGIN_PAGE_TITLE)

    home_page.click_my_account()
    expect(page).to_have_title(messages.LOGIN_PAGE_TITLE)
