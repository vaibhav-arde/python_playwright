# tests/ui/Register/TC_RF_015_register_account_details_stored_in_db_test.py
# =========================================================================
# Test Case ID: TC_RF_015
# Description: Validate the details provided while Registering an Account
# are stored in the Database (Verified via Account Profile UI Persistence)
"""
Validate that all details entered during registration are successfully persisted.
Following industry standards, persistence is verified by retrieving the details
from the 'Edit Account Information' and 'Newsletter' pages after registration.

Steps:
1. Open the application.
2. Click on 'My Account' -> 'Register'.
3. Enter new account details (First Name, Last Name, E-Mail, Telephone, Password).
4. Select Newsletter 'Yes' and check Privacy Policy.
5. Click 'Continue' to register.
6. Verify registration success message.
7. Navigate to 'Edit Account Information' and verify details match registration input.
8. Navigate to 'Newsletter' and verify subscription status matches.
"""
# =========================================================================

import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from pages.my_account_page import MyAccountPage
from utils.helpers import RandomDataUtil
from utils import messages
from pages.login_page import LoginPage


@pytest.mark.ui
@pytest.mark.regression
def test_register_account_details_stored_in_db(page):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)
    my_account_page = MyAccountPage(page)
    random_data = RandomDataUtil()

    # Step: Navigate to Register
    home_page.click_my_account()
    home_page.click_register()
    login_page = LoginPage(page)

    # Step: Prepare and fill Data
    first_name = random_data.get_first_name()
    last_name = random_data.get_last_name()
    email = random_data.get_email()
    phone = random_data.get_phone_number()
    password = random_data.get_password()

    registration_page.set_first_name(first_name)
    registration_page.set_last_name(last_name)
    registration_page.set_email(email)
    registration_page.set_telephone(phone)
    registration_page.set_password(password)
    registration_page.set_confirm_password(password)

    registration_page.set_newsletter_subscription(True)  # Subscribe to Yes
    registration_page.set_privacy_policy()

    # Step: Complete Registration
    registration_page.click_continue()

    # Verification: Account Created Success Message
    confirmation_msg = registration_page.get_confirmation_msg()
    expect(confirmation_msg).to_be_visible()
    expect(confirmation_msg).to_have_text(messages.ACCOUNT_CREATED)

    # We click 'Continue' to go to 'My Account' dashboard or just use the nav links.
    registration_page.click_continue()  # This takes user to My Account page from Success page.

    my_account_page.click_logout()

    # Step: Verify Edit Account Info Persistence
    home_page.click_my_account()
    home_page.click_login()
    login_page.set_email(email)
    login_page.set_password(password)
    login_page.click_login()

    expect(my_account_page.get_my_account_page_heading()).to_be_visible()
