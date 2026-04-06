"""(TS_001) 
Register Functionality

Validate Registring an Account, by filling 'Password' field and not filling 'Password Confirm' field
1. Open the Application (https://demo.opencart.com) in any Browser
2. Click on 'My Account' Drop menu
3. Click on 'Register' option 
4. Enter new Account Details into all the Fields (First Name, Last Name, E-Mail,Telephone, Password, Newsletter and  Privacy Policy Fields)
5. Don't enter into 'Password Confirm' field
6. Click on 'Continue' button (ER-1)
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from utils.helpers import RandomDataUtil


@pytest.mark.sanity
@pytest.mark.regression
def test_register_without_confirm_password(page):
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

    registration_page.set_privacy_policy()
    registration_page.click_continue()
    expect(registration_page.get_confirm_password_error()).to_be_visible()



