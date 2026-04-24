"""
1. Click on 'Site Map' footer option
2. Click on 'Account Information' link in the displayed 'Site Map' page (Validate ER-1)
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.edit_account_page import EditAccountPage
from utils.constants import UIRoutes


@pytest.mark.ui
def test_edit_account_info_right_column(authenticated_page):
    page = authenticated_page
    home_page = HomePage(page)
    edit_account_page = EditAccountPage(page)

    home_page.click_sitemap()
    home_page.click_account_information()

    expect(edit_account_page.get_page_heading()).to_be_visible()
    expect(page).to_have_url(UIRoutes.EDIT_ACCOUNT_INFORMATION)
