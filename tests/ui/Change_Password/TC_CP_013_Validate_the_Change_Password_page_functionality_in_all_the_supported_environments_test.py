import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.change_password_page import ChangePasswordPage
from utils.user_registration import generate_user_data, register_user
from pages.registration_page import RegistrationPage
from utils import change_password_constants


@pytest.mark.ui
@pytest.mark.critical
def test_validate_the_change_password_page_functionality_in_all_the_supported_environments(page):
    """
    Test Case: TC_CP_013 - Validate the Change Password page functionality in all the supported environments
    """
    HomePage(page)
    my_account_page = MyAccountPage(page)
    registration_page = RegistrationPage(page)
    change_password_page = ChangePasswordPage(page)

    # Step 1: Generate random user data and register
    user_data = generate_user_data()
    register_user(page, user_data)

    # After registration, click continue to go to My Account
    registration_page.click_continue()

    # Step 2: Navigate to Change Password page
    # 1. Click on 'Password' Right Column option
    my_account_page.click_password_right_column()

    # Step 3: Check the 'Change Password' page functionality (Validate ER-1)
    new_password_data = generate_user_data()
    new_password = new_password_data[change_password_constants.PASSWORD_FIELD_TYPE]
    change_password_page.fill_new_password_details(new_password)

    # Acceptance Criteria: 'Change Password' page functionality should work correctly
    expect(change_password_page.get_success_message()).to_have_text(
        change_password_constants.SUCCESS_PASSWORD_UPDATED
    )
