"""
1. Click on 'My Account' dropdown
2. Select 'My Account' option
3. Click on 'Edit your account information' link on the displayed 'My Account' page
4. Observe all the fields - First Name, Last Name, E-Mail and Telephone in the displayed 'My Account Information' page (Validate ER-1)
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.edit_account_page import EditAccountPage
from utils.constants import ACCOUNT_FIELDS


@pytest.mark.ui
def test_edit_account_info_placeholders(authenticated_page):
    page = authenticated_page
    home_page = HomePage(page)
    my_account_page = MyAccountPage(page)
    edit_account_page = EditAccountPage(page)

    home_page.click_my_account()
    home_page.click_my_account_option()
    my_account_page.click_edit_account_info()
    expect(edit_account_page.get_page_heading()).to_be_visible()

    edit_account_page.clear_account_info_fields()

    for field_id, expected in ACCOUNT_FIELDS.items():
        actual = edit_account_page.get_placeholder(field_id)
        expected_placeholder = expected["placeholder"]
        assert (
            actual == expected_placeholder
        ), f"{field_id} placeholder mismatch: expected '{expected_placeholder}', got '{actual}'"
