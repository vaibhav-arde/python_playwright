"""
Click on 'My Account' dropdown
Select 'My Account' option
Click on 'Edit your account information' link on the displayed 'My Account' page
Update the fields in the 'My Account Information' page
Click on 'Back' button (Validate ER-1)
Click on 'Edit your account information' link again (Validate ER-2)
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.edit_account_page import EditAccountPage
from utils.random_test_data import RandomTestData


@pytest.mark.ui
def test_edit_account_info_back_button(authenticated_page):
    page = authenticated_page

    home_page = HomePage(page)
    my_account_page = MyAccountPage(page)
    edit_account_page = EditAccountPage(page)

    # Navigate
    home_page.click_my_account()
    home_page.click_my_account_option()
    my_account_page.click_edit_account_info()

    expect(edit_account_page.get_page_heading()).to_be_visible()

    # ✅ Step 1: Capture original data FIRST
    original_data = edit_account_page.get_account_information()

    # Step 2: Update fields
    updated_user = RandomTestData.get_user()
    edit_account_page.update_account_information(updated_user)

    # Step 3: Click Back (changes should NOT persist)
    edit_account_page.click_back()

    # Step 4: Reopen Edit page
    my_account_page.click_edit_account_info()
    expect(edit_account_page.get_page_heading()).to_be_visible()

    # Step 5: Validate data is unchanged
    current = edit_account_page.get_account_information()

    for key in original_data:
        assert (
            current[key] == original_data[key]
        ), f"{key} changed: expected {original_data[key]}, got {current[key]}"
