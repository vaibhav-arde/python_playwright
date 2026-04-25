import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.change_password_page import ChangePasswordPage
from utils.user_registration import generate_user_data, register_user
from pages.registration_page import RegistrationPage
from utils import change_password_constants
from utils import messages


@pytest.mark.ui
def test_validate_breadcrumb_in_change_password(page):
    """
    Test Case: TC_CP_008 - Validate the text entered into the fields in Change Password field is toggled to hide its display
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

    # 1. Click on 'Password' Right Column option
    my_account_page.click_password_right_column()

    expect(change_password_page.get_breadcrumb_items()).to_be_visible()
    expect(change_password_page.get_breadcrumb_items()).to_contain_text(
        messages.ACCOUNT_CHANGE_PASSWORD_BREADCRUMB
    )

    change_password_page.get_account_breadcrumb()

    expect(page).to_have_title(messages.ACCOUNT_PAGE_TITLE)

    page.go_back()

    change_password_page.get_change_password_breadcrumb()

    expect(page).to_have_title(change_password_constants.CHANGE_PASSWORD_PAGE_TITLE)
