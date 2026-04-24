import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.change_password_page import ChangePasswordPage
from pages.login_page import LoginPage
from utils.user_registration import generate_user_data, register_user
from pages.registration_page import RegistrationPage

@pytest.mark.ui
def test_validate_password_field_display_toggled(page):
    """
    Test Case: TC_CP_008 - Validate the text entered into the fields in Change Password field is toggled to hide its display
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

    change_password_page.fill_new_password(user_data["password"])

    # 2. Check whether the Password fields in the displayed 'Change Password' page are marked as mandatory
    # Acceptance Criteria: All the fields in the 'Change Password' page should be marked as mandatory using the Red color * symbol
    expect(change_password_page.get_password_field()).to_have_attribute("type", "password")
    expect(change_password_page.get_confirm_password_field()).to_have_attribute("type", "password")


