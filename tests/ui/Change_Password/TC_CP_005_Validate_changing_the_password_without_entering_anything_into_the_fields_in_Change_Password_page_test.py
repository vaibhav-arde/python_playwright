import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.change_password_page import ChangePasswordPage
from pages.registration_page import RegistrationPage
from utils.user_registration import generate_user_data, register_user
from utils import messages


@pytest.mark.ui
def test_validate_change_password_without_entering_anything_into_the_fields_in_Change_Password_page(
    page,
):
    """
    Test Case: TC_CP_004 - Validate changing the password using credentials from Config
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

    my_account_page.click_password_right_column()
    change_password_page.fill_new_password_details(messages.EMPTY_FIELDS)
    expect(change_password_page.get_pass_required_error()).to_be_visible()
