"""
Click on 'My Account' dropdown
Select 'My Account' option
Click on 'Edit your account information' link on the displayed 'My Account' page
Update the 'E-Mail' field in the 'My Account Information' page with invalid email format (Refer Test Data)
Click on 'Continue' button

"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.edit_account_page import EditAccountPage
from utils.constants import InvalidEmail


@pytest.mark.ui
@pytest.mark.parametrize("email, expected_error", InvalidEmail.test_data)
def test_invalid_email_format(authenticated_page, email, expected_error):
    page = authenticated_page

    home_page = HomePage(page)
    my_account_page = MyAccountPage(page)
    edit_account_page = EditAccountPage(page)

    # Directly go to My Account (already logged in)
    home_page.click_my_account()
    home_page.click_my_account_option()

    my_account_page.click_edit_account_info()
    expect(edit_account_page.get_page_heading()).to_be_visible()

    # Invalid email test
    edit_account_page.clear_email_field()
    edit_account_page.update_email(email)
    edit_account_page.click_continue()

    actual_error = edit_account_page.get_email_validation_message()

    assert expected_error in actual_error, f"Expected '{expected_error}', got '{actual_error}'"
