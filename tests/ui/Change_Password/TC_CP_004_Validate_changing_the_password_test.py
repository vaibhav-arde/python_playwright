import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from pages.my_account_page import MyAccountPage
from pages.change_password_page import ChangePasswordPage
from pages.login_page import LoginPage
from pages.logout_page import LogoutPage
from utils import messages
from utils.user_registration import generate_user_data, register_user


@pytest.mark.ui
def test_change_password(page):
    """
    Test Case: TC_CP_004 - Validate changing the password using generated user data
    """
    home_page = HomePage(page)
    my_account_page = MyAccountPage(page)
    login_page = LoginPage(page)
    logout_page = LogoutPage(page)
    change_password_page = ChangePasswordPage(page)
    registration_page = RegistrationPage(page)

    # Step 1: Generate random user data and register
    user_data = generate_user_data()
    register_user(page, user_data)

    # After registration, click continue to go to My Account

    registration_page.click_continue()

    # Step 2: Navigate to Change Password page
    my_account_page.click_password_right_column()

    # Step 3: Generate a NEW password for the change
    new_password_data = generate_user_data()
    new_password = new_password_data["password"]

    # Step 4: Perform password change
    change_password_page.fill_new_password_details(new_password)
    expect(change_password_page.get_success_message()).to_have_text(
        messages.SUCCESS_PASSWORD_UPDATED
    )

    # Step 5: Verify login with OLD password fails
    my_account_page.click_logout()
    logout_page.click_continue()
    home_page.click_my_account()
    home_page.click_login()

    login_page.login(user_data["email"], user_data["password"])
    expect(login_page.get_login_error()).to_contain_text(messages.WARN_LOGIN_ERROR)

    # Step 6: Verify login with NEW password succeeds
    login_page.login(user_data["email"], new_password)
    expect(page).to_have_title(messages.ACCOUNT_PAGE_TITLE)
