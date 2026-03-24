"""
1. Click on 'My Account' Drop menu
2. Click on 'Register' option 
3. Enter new Account Details into the Mandatory Fields (First Name, Last Name, E-Mail,Telephone, Password, Password Confirm and  Privacy Policy Fields)
4. Click on 'Continue' button (ER-1)
5. Click on 'Continue' button that is displayed in the 'Account Success' page (ER-2)
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from utilities.random_data_util import RandomDataUtil

@pytest.mark.sanity
def test_register_with_mandatory_fields_only(page):
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
    confirm_password = password

    registration_page.set_first_name(first_name)
    registration_page.set_last_name(last_name)
    registration_page.set_email(email)
    registration_page.set_telephone(phone)
    registration_page.set_password(password)
    registration_page.set_confirm_password(confirm_password)
    registration_page.set_privacy_policy()
    registration_page.click_continue()

    confirmation_msg = registration_page.get_confirmation_msg()
    expect(confirmation_msg).to_have_text("Your Account Has Been Created!")

    