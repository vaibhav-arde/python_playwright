"""
1. Click on 'My Account' dropdown
2. Select 'My Account' option
3. Click on 'Edit your account information' link on the displayed 'My Account' page
4. Clear all the fields - First Name, Last Name, E-Mail and Telephone in the displayed 'My Account Information' page
5. Click on 'Continue' button (Validate ER-1)
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.edit_account_page import EditAccountPage
from utils import messages


@pytest.mark.ui
def test_clear_account_info_fields(authenticated_page):
    page = authenticated_page
    home_page = HomePage(page)
    my_account_page = MyAccountPage(page)
    edit_account_page = EditAccountPage(page)

    home_page.click_my_account()
    home_page.click_my_account_option()

    my_account_page.click_edit_account_info()
    expect(edit_account_page.get_page_heading()).to_be_visible()

    edit_account_page.clear_account_info_fields()
    edit_account_page.click_continue()

    expect(edit_account_page.err_firstname).to_contain_text(messages.WARN_FIRST_NAME)
    expect(edit_account_page.err_lastname).to_contain_text(messages.WARN_LAST_NAME)
    expect(edit_account_page.err_email).to_contain_text(messages.WARN_EMAIL)
    expect(edit_account_page.err_telephone).to_contain_text(messages.WARN_TELEPHONE)
