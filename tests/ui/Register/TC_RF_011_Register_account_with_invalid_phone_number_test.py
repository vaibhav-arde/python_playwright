"""
1. Click on 'My Account' Drop menu
2. Click on 'Register' option
3. Enter new  Account Details into all the Fields (First Name, Last Name,E-Mail, Password, Password Confirm, Newsletter and  Privacy Policy Fields)
4. Enter invalid phone number into the Telephone Field - <Refer Test Data>
5. Click on 'Continue' button (ER-1)
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from utils.constants import INVALID_PHONE_NUMBERS
from utils.helpers import RandomDataUtil
from utils.messages import WARN_TELEPHONE


@pytest.mark.bug
@pytest.mark.xfail(
    reason="Bug: Invalid phone numbers are accepted as valid, no immediate fix planned"
)
@pytest.mark.sanity
@pytest.mark.parametrize("phone", INVALID_PHONE_NUMBERS)
def test_register_account_with_invalid_phone_number(page, phone):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    home_page.click_my_account()
    home_page.click_register()

    random_data = RandomDataUtil()

    first_name = random_data.get_first_name()
    last_name = random_data.get_last_name()
    email = random_data.get_email()
    password = random_data.get_password()
    confirm_password = password

    registration_page.set_first_name(first_name)
    registration_page.set_last_name(last_name)
    registration_page.set_email(email)
    registration_page.set_telephone(phone)
    registration_page.set_password(password)
    registration_page.set_confirm_password(confirm_password)
    registration_page.set_privacy_policy()
    registration_page.click_continue()

    actual_error_msg = registration_page.get_telephone_error_msg()
    expect(actual_error_msg).to_have_text(WARN_TELEPHONE)
