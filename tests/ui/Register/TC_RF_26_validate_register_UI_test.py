"""(TS_001) 
Register Functionality 
Validate the UI of the 'Register Account' page
1. Open the Application (https://demo.opencart.com) in any Browser
2. Click on 'My Account' Drop menu
3. Click on 'Register' option 
4. Verify the UI of the 'Register Account' page (ER-1)
"""

import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage

@pytest.mark.sanity
@pytest.mark.regression
def test_register_ui(page):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    home_page.click_my_account()
    home_page.click_register()

    # Verify the UI of the 'Register Account' page
    registration_page.validate_register_ui() 
