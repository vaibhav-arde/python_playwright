"""
1. Click on 'My Account' Drop menu
2. Click on 'Register' option
3. Enter new Account Details into all the Fields
   (First Name, Last Name, E-Mail, Telephone, Password, Password Confirm, Newsletter)
4. Don't select the 'Privacy Policy' checkbox option
5. Click on 'Continue' button (ER-1)

Expected Result:
Warning message - 'Warning: You must agree to the Privacy Policy!' should be displayed
"""

import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from utils.helpers import RandomDataUtil
from utils.messages import PRIVACY_POLICY_WARNING_MSG


@pytest.mark.sanity
def test_register_without_privacy_policy(page):

    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    # Step 1 & 2
    home_page.click_my_account()
    home_page.click_register()

    # Step 3: Enter details
    random_data = RandomDataUtil()

    first_name = random_data.get_first_name()
    last_name = random_data.get_last_name()
    email = random_data.get_email()
    telephone = random_data.get_phone_number()
    password = random_data.get_password()

    registration_page.set_first_name(first_name)
    registration_page.set_last_name(last_name)
    registration_page.set_email(email)
    registration_page.set_telephone(telephone)
    registration_page.set_password(password)
    registration_page.set_confirm_password(password)

    # ❌ Step 4: DO NOT select privacy policy

    # Step 5
    registration_page.click_continue()

    # Validation
    actual_warning = registration_page.get_privacy_policy_warning()
    expect(actual_warning).to_have_text(PRIVACY_POLICY_WARNING_MSG)
