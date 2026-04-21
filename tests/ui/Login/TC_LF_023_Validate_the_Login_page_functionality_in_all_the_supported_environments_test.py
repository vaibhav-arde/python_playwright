import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.constants import UIRoutes
from utils import messages


@pytest.mark.ui
@pytest.mark.cross_browser
def test_validate_the_login_page_functionality_in_all_the_supported_environments(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    # --- Step 1: Click on 'My Account' Dropmenu ---
    home_page.click_my_account()

    # --- Step 2: Click on 'Login' option (ER-1) ---
    home_page.click_login()

    # --- Acceptance Criteria: Login page loads correctly in this browser ---
    expect(page).to_have_url(UIRoutes.LOGIN)
    expect(page).to_have_title(messages.LOGIN_PAGE_TITLE)
    expect(login_page.get_email_field()).to_be_visible()
    expect(login_page.get_password_field()).to_be_visible()
    expect(login_page.get_login_button()).to_be_visible()
