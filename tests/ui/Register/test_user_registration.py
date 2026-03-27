"""
Test Case: User Registration Functionality

===========================================
Test Steps
===========================================
1. Navigate to Home page → My Account → Register.
2. Fill registration form with random data.
3. Accept Privacy Policy and submit.
4. Verify account creation confirmation message.
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from utils.helpers import RandomDataUtil


@pytest.mark.sanity
@pytest.mark.regression
def test_user_registration(page):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    home_page.click_my_account()
    home_page.click_register()

    random_data = RandomDataUtil()

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

    registration_page.set_privacy_policy()
    registration_page.click_continue()

    confirmation_msg = registration_page.get_confirmation_msg()
    expect(confirmation_msg).to_have_text("Your Account Has Been Created!")

def test_user_registration_empty_fields(page):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    home_page.click_my_account()
    home_page.click_register()

    registration_page.click_continue()

    assert registration_page.error_msg_visible()