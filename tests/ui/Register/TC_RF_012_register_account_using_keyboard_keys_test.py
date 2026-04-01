# tests/ui/Register/TC_RF_012_register_account_using_keyboard_keys_test.py
# =========================================================================
# Test Case ID: TC_RF_012
# Description: Validate Registering an Account by using the Keyboard keys
# =========================================================================

import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from utils.helpers import RandomDataUtil
from utils.constants import Messages

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
    
    # Fill First Name 
    page.keyboard.type(random_data.get_first_name())
    page.keyboard.press("Tab") #move to last name
    
    # Fill Last Name and Tab
    page.keyboard.type(random_data.get_last_name())
    page.keyboard.press("Tab") # move to email
    
    # Fill E-Mail and Tab
    page.keyboard.type(random_data.get_email())
    page.keyboard.press("Tab") # move to phone_number
    
    # Fill Telephone and Tab
    page.keyboard.type(random_data.get_phone_number())
    page.keyboard.press("Tab") # move to password
    
    # Fill Password and Tab
    test_password = random_data.get_password()
    page.keyboard.type(test_password)
    page.keyboard.press("Tab") # move to confirm password
    
    # Fill Password Confirm and Tab
    page.keyboard.type(test_password)
    page.keyboard.press("Tab") # move to newsletter
    
    # Newsletter Selection (Default is No)
    page.keyboard.press("Tab") # move to privacy policy
    
    # Privacy Policy Checkbox (Use Spacebar to check)
    page.keyboard.press("Tab") # Move to Privacy Policy checkbox
    page.keyboard.press("Space") # check privacy policy
    
    # Click on 'Continue' button (Use Enter to submit)
    page.keyboard.press("Tab") # Move to Continue button
    page.keyboard.press("Enter")

    # Verification: User should be taken to 'Account Success' page
    confirmation_msg = registration_page.get_confirmation_msg()
    expect(confirmation_msg).to_be_visible()
    expect(confirmation_msg).to_have_text(Messages.ACCOUNT_CREATED)

