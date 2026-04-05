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
from utils.config import Config
from utils.message import Message
from utils.constants import UserDetails
from utils.constants import InvalidEmail
from utils.constants import InvalidPassword


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
    expect(confirmation_msg).to_have_text(Message.registration_success)


def test_user_registration_empty_fields(page):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    home_page.click_my_account()
    home_page.click_register()

    registration_page.click_continue()

    registration_page.error_msg_visible()


def test_validate_password_and_confirm_password(page):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    home_page.click_my_account()
    home_page.click_register()

    random_data = RandomDataUtil()

    first_name = random_data.get_first_name()
    last_name = random_data.get_last_name()
    email = random_data.get_email()
    phone = random_data.get_phone_number()
    password = InvalidPassword.password
    confirm_password = InvalidPassword.confirm_password

    registration_page.set_first_name(first_name)
    registration_page.set_last_name(last_name)
    registration_page.set_email(email)
    registration_page.set_telephone(phone)
    registration_page.set_password(password)
    registration_page.set_confirm_password(confirm_password)

    registration_page.set_privacy_policy()
    registration_page.click_continue()

    password_mismatch_error = registration_page.get_password_mismatch_error()
    expect(password_mismatch_error).to_have_text(Message.password_not_match_error)


def test_user_registration_empty_fields(page):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    home_page.click_my_account()
    home_page.click_register()

    registration_page.click_continue()

    registration_page.error_msg_visible()


def test_account_validation_with_existing_account_details(page):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    home_page.click_my_account()
    home_page.click_register()

    first_name = UserDetails.first_name
    last_name = UserDetails.last_name
    email = UserDetails.email
    phone = UserDetails.telephone
    password = UserDetails.password
    confirm_password = UserDetails.confirm_password

    registration_page.set_first_name(first_name)
    registration_page.set_last_name(last_name)
    registration_page.set_email(email)
    registration_page.set_telephone(phone)
    registration_page.set_password(password)
    registration_page.set_confirm_password(confirm_password)

    registration_page.set_privacy_policy()
    registration_page.click_continue()

    email_already_exist_error = registration_page.get_email_already_exist_error()
    expect(email_already_exist_error).to_have_text(Message.email_already_exist_error)


@pytest.mark.parametrize("invalid_email, expected_msg", InvalidEmail.test_data)
def test_account_validation_with_invalid_email(page, invalid_email, expected_msg):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    home_page.click_my_account()
    home_page.click_register()

    random_data = RandomDataUtil()

    first_name = random_data.get_first_name()
    last_name = random_data.get_last_name()
    phone = random_data.get_phone_number()
    password = random_data.get_password()
    confirm_password = random_data.get_password()

    registration_page.set_first_name(first_name)
    registration_page.set_last_name(last_name)
    registration_page.set_email(invalid_email)
    registration_page.set_telephone(phone)
    registration_page.set_password(password)
    registration_page.set_confirm_password(confirm_password)

    registration_page.set_privacy_policy()
    registration_page.click_continue()

    validation_msg = registration_page.get_email_validation_message()
    assert expected_msg in validation_msg, (
        f"Expected '{expected_msg}' in validation message, got: '{validation_msg}'"
    )
