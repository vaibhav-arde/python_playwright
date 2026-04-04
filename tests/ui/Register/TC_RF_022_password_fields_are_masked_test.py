"""
1. Click on 'My Account' Drop menu
2. Click on 'Register' option 
3. Enter some Password text into the 'Password' and 'Password Confirm' fields

Expected Result:
Password text should be hidden (input type = password)
"""

import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from utils.constants import VALID_PASSWORD


@pytest.mark.sanity
def test_password_fields_are_masked(page):

    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    # Step 1 & 2
    home_page.click_my_account()
    home_page.click_register()

    # Step 3
    registration_page.set_password(VALID_PASSWORD)
    registration_page.set_confirm_password(VALID_PASSWORD)

    # Validation: check input type is password (masked)
    password_type = registration_page.get_password_field_type()
    confirm_password_type = registration_page.get_confirm_password_field_type()

    assert password_type == "password"
    assert confirm_password_type == "password"