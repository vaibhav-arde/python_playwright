import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.config import Config
from utils import change_password_constants


@pytest.mark.xfail
@pytest.mark.ui
def test_validate_the_password_is_not_visible_in_the_page_source(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    # 1. Click on 'My Account' Dropmenu and navigate to Login page
    home_page.click_my_account()
    home_page.click_login()

    # 2. Enter any text into the 'Password' field
    login_page.get_password_field().fill(Config.password)

    # 3. Inspect the Password text field (ER-1)
    # Acceptance Criteria: Password text should not be visible in the Page source
    expect(login_page.get_password_field()).not_to_have_attribute(
        change_password_constants.VALUE_ATTRIBUTE, Config.password
    )

    # 4. Click on 'Login' button and inspect the Password text field (ER-1)
    login_page.click_login()

    # 5. Acceptance Criteria: Password text should not be visible in the Page source
    expect(login_page.get_password_field()).not_to_have_attribute(
        change_password_constants.VALUE_ATTRIBUTE, Config.password
    )
