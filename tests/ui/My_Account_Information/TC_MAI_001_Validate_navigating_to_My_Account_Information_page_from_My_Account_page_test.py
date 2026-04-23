"""
Click on 'My Account' dropmenu
Select 'My Account' option
Click on 'Edit your account information' link on the displayed 'My Account' page (Validate ER-1)
"""

import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.login_page import LoginPage
from pages.edit_account_page import EditAccountPage
from utils.constants import UIRoutes


@pytest.mark.ui
def test_validate_navigating_to_my_account_information_page_from_my_account_page(
    page, registered_user
):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    my_account_page = MyAccountPage(page)
    edit_account_page = EditAccountPage(page)

    # Step 1: login using the valid credentials to ensure active session and clean context
    home_page.click_my_account()
    home_page.click_login()

    login_page.login_user(registered_user)
    expect(my_account_page.get_my_account_page_heading()).to_be_visible()
    my_account_page.click_edit_account_info()

    expect(edit_account_page.get_page_heading()).to_be_visible()
    expect(page).to_have_url(UIRoutes.EDIT_ACCOUNT_INFORMATION)
