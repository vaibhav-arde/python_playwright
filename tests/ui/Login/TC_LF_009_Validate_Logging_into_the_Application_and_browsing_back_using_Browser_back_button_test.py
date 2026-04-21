import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage


@pytest.mark.ui
def test_validate_logging_and_browsing_back(page, registered_user):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    my_account_page = MyAccountPage(page)

    # 1. Click on 'My Account' Dropmenu and navigate to Login page
    home_page.click_my_account()
    home_page.click_login()

    # 2. Enter valid credentials and login
    # Data is provided by the registered_user fixture
    login_page.login(registered_user["email"], registered_user["password"])

    # 3. Click on Browser back button
    page.go_back()

    # 4. Verify session is still active by checking the "My Account" dropdown for the 'Logout' option
    home_page.click_my_account()
    expect(my_account_page.get_logout_link()).to_be_visible()
