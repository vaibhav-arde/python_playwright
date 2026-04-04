"""(TS_001) 
Register Functionality

Validate all the fields in the Register Account page have the proper placeholders

1. Open the Application (https://demo.opencart.com) in any Browser
2. Click on 'My Account' Drop menu
3. Click on 'Register' option 
4. View the First Name, Last Name, E-Mail, Telephone, Password, Password Confirm fields for Placeholders (ER-1)"""

import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage

@pytest.mark.sanity
@pytest.mark.regression
def test_register_field_placeholders(page):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    home_page.click_my_account()
    home_page.click_register()

    # Validate All Placeholders
    registration_page.validate_all_placeholders()

