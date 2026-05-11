# tests/ui/Register/TC_RF_012_register_account_using_keyboard_keys_test.py
# =========================================================================
# Test Case ID: TC_RF_012
# Description: Validate Registering an Account by using the Keyboard keys
# =========================================================================

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from utils import messages
from utils.helpers import RandomDataUtil


@pytest.mark.ui
@pytest.mark.regression
def test_register_account_using_keyboard_keys(page):
    """
    Validate registration process using only keyboard interactions (Tab, Space, Enter).
    Ensures all input data is generated dynamically.
    """
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)
    random_data = RandomDataUtil()

    home_page.click_my_account()
    home_page.click_register()

    # Enter new Account Details into all the Fields using Keyboard keys
    # Focus on the first field to start the keyboard sequence
    registration_page.txt_firstname.focus()

    # Generate common password
    test_password = random_data.get_password()

    # Define sequence of input actions
    form_fields_data = [
        random_data.get_first_name(),
        random_data.get_last_name(),
        random_data.get_email(),
        random_data.get_phone_number(),
        test_password,  # Password
        test_password,  # Password Confirm
    ]

    # Type value and Tab to the next field
    for field_value in form_fields_data:
        page.keyboard.type(field_value)
        page.keyboard.press("Tab")

    # Navigate past Newsletter selection to Privacy Policy checkbox (2 tabs)
    for _ in range(2):
        page.keyboard.press("Tab")

    # Check Privacy Policy
    page.keyboard.press("Space")

    # Navigate to Continue button and submit
    page.keyboard.press("Tab")
    page.keyboard.press("Enter")

    # Verification: User should be taken to 'Account Success' page
    confirmation_msg = registration_page.get_confirmation_msg()
    expect(confirmation_msg).to_be_visible()
    expect(confirmation_msg).to_have_text(messages.ACCOUNT_CREATED)
