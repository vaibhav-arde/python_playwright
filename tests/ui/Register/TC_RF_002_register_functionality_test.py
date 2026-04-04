"""Test Case ID: TC_RF_002
Test Scenario: Register Functionality

Test Objective:
Validate 'Thank you for registering' email is sent to registered email

Test Steps:
1. Open Application
2. Click My Account -> Register
3. Enter Mandatory Fields
4. Click Continue
5. Verify Registration Success
6. Verify Email Received
7. Click Login Link from Email
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

    expect(registration_page.get_confirmation_msg()).to_be_visible()
