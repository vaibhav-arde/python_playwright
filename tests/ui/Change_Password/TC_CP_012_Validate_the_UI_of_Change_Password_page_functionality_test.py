import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.change_password_page import ChangePasswordPage
from utils.user_registration import generate_user_data, register_user
from pages.registration_page import RegistrationPage
from utils import change_password_constants


@pytest.mark.ui
def test_validate_the_ui_of_change_password_page_functionality(page):
    """
    Test Case: TC_CP_012 - Validate the UI of Change Password page functionality
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
    my_account_page.click_password_right_column()

    # Step 3: Validate UI Elements
    # 1. Validate Page Title
    expect(page).to_have_title(change_password_constants.CHANGE_PASSWORD_PAGE_TITLE)

    # 3. Validate Legend
    expect(change_password_page.legend_your_password).to_be_visible()
    expect(change_password_page.legend_your_password).to_have_text(
        change_password_constants.LEGEND_YOUR_PASSWORD
    )

    # 4. Validate Labels and Input Fields
    expect(change_password_page.lbl_password).to_be_visible()
    expect(change_password_page.lbl_password).to_have_text(
        change_password_constants.PASSWORD_FIELD_TEXT
    )
    expect(change_password_page.txt_password).to_be_visible()
    expect(change_password_page.txt_password).to_have_attribute(
        change_password_constants.PLACEHOLDER_ATTRIBUTE,
        change_password_constants.PASSWORD_FIELD_PLACEHOLDER,
    )
    expect(change_password_page.txt_password).to_have_attribute(
        change_password_constants.TYPE_ATTRIBUTE, change_password_constants.PASSWORD_FIELD_TYPE
    )

    expect(change_password_page.lbl_confirm_password).to_be_visible()
    expect(change_password_page.lbl_confirm_password).to_have_text(
        change_password_constants.PASSWORD_CONFIRM_FIELD_TEXT
    )
    expect(change_password_page.txt_confirm_password).to_be_visible()
    expect(change_password_page.txt_confirm_password).to_have_attribute(
        change_password_constants.PLACEHOLDER_ATTRIBUTE,
        change_password_constants.PASSWORD_CONFIRM_FIELD_TEXT,
    )
    expect(change_password_page.txt_confirm_password).to_have_attribute(
        change_password_constants.TYPE_ATTRIBUTE, change_password_constants.PASSWORD_FIELD_TYPE
    )

    # 5. Validate Buttons
    expect(change_password_page.btn_back).to_be_visible()
    expect(change_password_page.btn_continue).to_be_visible()
    expect(change_password_page.btn_continue).to_have_attribute(
        change_password_constants.VALUE_ATTRIBUTE, change_password_constants.BUTTON_VALUE
    )

    # 6. Validate Mandatory Field Markers
    assert change_password_page.is_field_mandatory(change_password_constants.PASSWORD_FIELD_TYPE), (
        change_password_constants.ASSERT_PASSWORD_REQUIRED
    )
    assert change_password_page.is_field_mandatory(
        change_password_constants.CONFIRM_PASSWORD_FIELD_TYPE
    ), change_password_constants.ASSERT_PASSWORD_CONFIRM_REQUIRED
