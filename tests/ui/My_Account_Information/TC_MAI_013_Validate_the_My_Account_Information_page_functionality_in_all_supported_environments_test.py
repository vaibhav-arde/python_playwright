import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.edit_account_page import EditAccountPage


@pytest.mark.ui
@pytest.mark.cross_browser
def test_mai_013_page_functionality_in_all_supported_environments(authenticated_page):
    page = authenticated_page

    home_page = HomePage(page)
    my_account_page = MyAccountPage(page)
    edit_account_page = EditAccountPage(page)

    # Navigate
    home_page.click_my_account()
    home_page.click_my_account_option()
    my_account_page.click_edit_account_info()

    expect(edit_account_page.get_page_heading()).to_be_visible()
