"""
1. Click on 'My Account' dropdown
2. Select 'My Account' option
3. Click on 'Edit your account information' link on the displayed 'My Account' page
4. Check the Page Heading, Page URL and Page Title in the displayed 'My Account Information' page (Validate ER-1)
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.edit_account_page import EditAccountPage
from utils.constants import UIRoutes, MAI_TITLE


@pytest.mark.ui
def test_my_account_info_page_heading_title_and_url(authenticated_page):
    page = authenticated_page

    home_page = HomePage(page)
    my_account_page = MyAccountPage(page)
    edit_account_page = EditAccountPage(page)

    # Navigate
    home_page.click_my_account()
    home_page.click_my_account_option()
    my_account_page.click_edit_account_info()

    expect(edit_account_page.get_page_heading()).to_be_visible()
    expect(page).to_have_url(UIRoutes.EDIT_ACCOUNT_INFORMATION)
    expect(page).to_have_title(MAI_TITLE)
