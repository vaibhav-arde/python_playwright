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
from utils.constants import TestData

@pytest.mark.sanity
def test_password_fields_are_masked(page):

    home_page = HomePage(page)
    registration_page = RegistrationPage(page)
    VALID_PASSWORD = TestData.VALID_PASSWORD

    # Step 1 & 2
    home_page.click_my_account()
    home_page.click_register()

    # Step 3
    registration_page.set_password(TestData.VALID_PASSWORD)
    registration_page.set_confirm_password(TestData.VALID_PASSWORD)

    # ✅ Validation (updated)
    # expect(registration_page.txt_password).to_have_attribute("type", "password")
    # expect(registration_page.txt_confirm_password).to_have_attribute("type", "password")

    password_type = registration_page.get_element_attribute(registration_page.txt_password, "type")
    confirm_password_type = registration_page.get_element_attribute(registration_page.txt_confirm_password, "type")

    assert password_type == "password", "Password field is not masked"
    assert confirm_password_type == "password", "Confirm Password field is not masked"
