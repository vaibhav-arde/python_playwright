"""
1. Check the UI of the functionality related to 'My Account Information' page (Validate ER-1)
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.edit_account_page import EditAccountPage
from utils.constants import UIRoutes, MAI_TITLE


@pytest.mark.ui
def test_tc_mai_012_ui_validation(authenticated_page):
    page = authenticated_page

    home_page = HomePage(page)
    my_account_page = MyAccountPage(page)
    edit_account_page = EditAccountPage(page)

    # Navigate
    home_page.click_my_account()
    home_page.click_my_account_option()
    my_account_page.click_edit_account_info()

    # Page validation
    expect(edit_account_page.get_page_heading()).to_be_visible()
    expect(page).to_have_url(UIRoutes.EDIT_ACCOUNT_INFORMATION)
    expect(page).to_have_title(MAI_TITLE)

    # Breadcrumb
    edit_account_page.validate_breadcrumb()

    # Fields
    expect(edit_account_page.txt_firstname).to_be_visible()
    expect(edit_account_page.txt_lastname).to_be_visible()
    expect(edit_account_page.txt_email).to_be_visible()
    expect(edit_account_page.txt_telephone).to_be_visible()

    # Labels
    expect(edit_account_page.lbl_firstname).to_be_visible()
    expect(edit_account_page.lbl_lastname).to_be_visible()
    expect(edit_account_page.lbl_email).to_be_visible()
    expect(edit_account_page.lbl_telephone).to_be_visible()

    # Buttons
    expect(edit_account_page.btn_back).to_be_visible()
    expect(edit_account_page.btn_continue).to_be_visible()
