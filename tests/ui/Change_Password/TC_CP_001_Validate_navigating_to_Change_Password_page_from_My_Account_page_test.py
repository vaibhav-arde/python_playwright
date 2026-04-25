import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.registration_page import RegistrationPage
from utils.change_password_constants import CHANGE_PASSWORD_PAGE_TITLE
from utils.user_registration import generate_user_data, register_user


@pytest.mark.ui
def test_validate_navigating_to_change_password_page_from_my_account(page):
    """
    Test Case: TC_CP_001 - Validate navigating to Change Password page from My Account page
    """
    HomePage(page)
    my_account_page = MyAccountPage(page)
    registration_page = RegistrationPage(page)

    # Step 1: Generate random user data and register
    user_data = generate_user_data()
    register_user(page, user_data)

    # After registration, click continue to go to My Account

    registration_page.click_continue()

    # 3. Click on 'Change your password' link on the displayed 'My Account' page
    my_account_page.click_change_password_link()

    # 4. Acceptance Criteria - User should be navigated to 'Change Password' page
    expect(page).to_have_title(CHANGE_PASSWORD_PAGE_TITLE)
