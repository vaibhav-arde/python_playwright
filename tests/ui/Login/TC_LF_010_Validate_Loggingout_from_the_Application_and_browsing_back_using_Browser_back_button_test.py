import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from utils import messages
from utils import change_password_constants


@pytest.mark.ui
def test_validate_logging_out_and_browsing_back(page, registered_user):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    my_account_page = MyAccountPage(page)

    # 1. Reach the Login Page via My Account dropdown
    home_page.click_my_account()
    home_page.click_login()

    # 2. Login with valid credentials from fixture
    login_page.login(
        registered_user[change_password_constants.EMAIL_TXT],
        registered_user[change_password_constants.PASSWORD_FIELD_TYPE],
    )

    # 3. Click on 'My Account' Dropmenu and select 'Logout' option
    home_page.click_my_account()
    my_account_page.click_logout()

    # 4. Click on Browser back button
    page.go_back()

    # 5. Acceptance Criteria: User should not get logged in again.
    # To verify this, we refresh the page.
    # If the session is truly terminated, the user should be redirected to the Login page.
    page.reload()

    # Assert redirection to the Account Login page, proving the session is inactive
    expect(page).to_have_title(messages.LOGIN_PAGE_TITLE)
