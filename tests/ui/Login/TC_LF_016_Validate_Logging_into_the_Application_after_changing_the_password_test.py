import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from pages.change_password_page import ChangePasswordPage
from pages.logout_page import LogoutPage
from utils.config import Config
from utils import messages


@pytest.mark.ui
def test_validate_logging_into_the_application_after_changing_the_password(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    my_account_page = MyAccountPage(page)
    change_password_page = ChangePasswordPage(page)
    logout_page = LogoutPage(page)

    # 1. Click on 'My Account' Dropmenu and navigate to Login page
    home_page.click_my_account()
    home_page.click_login()

    # 2. Enter any text into the 'Password' field
    login_page.login(Config.email, Config.password)

    # 5. Click on 'Change your password' link
    my_account_page.click_change_password_link()

    # 6. Fill new password details and click continue
    change_password_page.fill_new_password_details(Config.password_change_new_password)

    my_account_page.click_logout()

    # 8. Click on 'Logout' link
    logout_page.click_continue()

    home_page.click_my_account()

    # 9. Click on 'Login' link
    home_page.click_login()

    # 10. Enter existing password details and click continue
    login_page.login(Config.email, Config.password)

    expect(page).to_have_title(messages.LOGIN_PAGE_TITLE)

    login_page.login(Config.email, Config.password_change_new_password)

    expect(page).to_have_title(messages.MY_ACCOUNT_HEADING)

    # --- Teardown: Revert password back to original to maintain test isolation ---
    my_account_page.click_change_password_link()
    change_password_page.fill_new_password_details(Config.password)

    # Logout after reverting password
    my_account_page.click_logout()
    logout_page.click_continue()
