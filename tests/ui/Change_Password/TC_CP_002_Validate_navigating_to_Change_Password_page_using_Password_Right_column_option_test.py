import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.registration_page import RegistrationPage
from utils.change_password_constants import CHANGE_PASSWORD_PAGE_TITLE
from utils.user_registration import generate_user_data, register_user


@pytest.mark.ui
def test_validate_navigating_to_change_password_page_using_password_option_at_right_column(page):
    """
    Test Case: TC_CP_002 - Validate navigating to Change Password page using Password Right column option
    """
    HomePage(page)
    my_account_page = MyAccountPage(page)
    registration_page = RegistrationPage(page)

    # Step 1: Generate random user data and register
    user_data = generate_user_data()
    register_user(page, user_data)

    # After registration, click continue to go to My Account

    registration_page.click_continue()

    # 1. Click on 'Password' Right Column option
    my_account_page.click_password_right_column()

    # 2. Acceptance Criteria - User should be navigated to 'Change Password' page
    expect(page).to_have_title(CHANGE_PASSWORD_PAGE_TITLE)
