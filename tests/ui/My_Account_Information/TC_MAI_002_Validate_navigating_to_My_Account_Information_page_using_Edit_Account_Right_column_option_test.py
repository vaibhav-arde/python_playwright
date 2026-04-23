"""
Click on 'Edit Account' Right Column option (Validate ER-1)

"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from pages.edit_account_page import EditAccountPage
from utils.constants import UIRoutes


@pytest.mark.ui
def test_edit_account_info_right_column(page, registered_user):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    my_account_page = MyAccountPage(page)
    edit_account_page = EditAccountPage(page)

    home_page.click_my_account()
    home_page.click_login()

    login_page.login(registered_user["email"], registered_user["password"])
    expect(my_account_page.get_my_account_page_heading()).to_be_visible()
    my_account_page.click_edit_right_column_option()

    expect(edit_account_page.get_page_heading()).to_be_visible()
    expect(page).to_have_url(UIRoutes.EDIT_ACCOUNT_INFORMATION)
