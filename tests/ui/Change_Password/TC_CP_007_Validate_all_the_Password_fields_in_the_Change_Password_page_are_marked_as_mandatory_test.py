import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.change_password_page import ChangePasswordPage
from pages.registration_page import RegistrationPage
from utils.user_registration import generate_user_data, register_user

@pytest.mark.ui
def test_validate_all_the_password_fields_in_the_Change_Password_page_are_marked_as_mandatory(page):
    """
    Test Case: TC_CP_007 - Validate all the Password fields in the Change Password page are marked as mandatory
    """
    home_page = HomePage(page)
    my_account_page = MyAccountPage(page)
    registration_page = RegistrationPage(page)
    change_password_page = ChangePasswordPage(page)

    # Step 1: Generate random user data and register
    user_data = generate_user_data()
    register_user(page, user_data)
    
    # After registration, click continue to go to My Account

    registration_page.click_continue()

    # 1. Click on 'Password' Right Column option
    my_account_page.click_password_right_column()

    # 2. Check whether the Password fields in the displayed 'Change Password' page are marked as mandatory
    # Acceptance Criteria: All the fields in the 'Change Password' page should be marked as mandatory using the Red color * symbol
    assert change_password_page.is_field_mandatory("password"), messages.ASSERT_PASSWORD_REQUIRED
    assert change_password_page.is_field_mandatory("confirm"), messages.ASSERT_PASSWORD_CONFIRM_REQUIRED


