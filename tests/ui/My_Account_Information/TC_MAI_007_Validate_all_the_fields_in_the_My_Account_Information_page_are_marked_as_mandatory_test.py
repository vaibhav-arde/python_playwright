"""
1. Click on 'My Account' dropdown
2. Select 'My Account' option
3. Click on 'Edit your account information' link on the displayed 'My Account' page
4. Check all the fields in the 'My Account Information' page - First Name, Last Name, E-Mail and Telephone (Validate ER-1)
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from pages.edit_account_page import EditAccountPage
from utils.constants import ACCOUNT_FIELDS


@pytest.mark.ui
def test_edit_account_info_mandatory_fields(page, registered_user):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    my_account_page = MyAccountPage(page)
    edit_account_page = EditAccountPage(page)

    home_page.click_my_account()
    home_page.click_login()

    login_page.login_user(registered_user)
    expect(my_account_page.get_my_account_page_heading()).to_be_visible()

    home_page.click_my_account()
    home_page.click_my_account_option()
    my_account_page.click_edit_account_info()
    expect(edit_account_page.get_page_heading()).to_be_visible()
    edit_account_page.verify_mandatory_fields(ACCOUNT_FIELDS)
