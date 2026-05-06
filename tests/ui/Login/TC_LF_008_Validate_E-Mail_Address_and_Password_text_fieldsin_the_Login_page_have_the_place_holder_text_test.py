import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils import messages


@pytest.mark.ui
def test_validate_login_field_placeholders(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    # 1. Navigate to Login Page
    home_page.click_my_account()
    home_page.click_login()
    expect(page).to_have_title(messages.LOGIN_PAGE_TITLE)

    # 2. Verify E-Mail Address placeholder
    expect(login_page.get_email_field()).to_have_attribute(
        "placeholder", messages.EMAIL_PLACEHOLDER
    )

    # 3. Verify Password placeholder
    expect(login_page.get_password_field()).to_have_attribute(
        "placeholder", messages.PASSWORD_PLACEHOLDER
    )
