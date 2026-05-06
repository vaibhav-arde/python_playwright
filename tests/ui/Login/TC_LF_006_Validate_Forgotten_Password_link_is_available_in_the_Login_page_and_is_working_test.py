import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils import messages


@pytest.mark.ui
def test_forgotten_password_link_visibility_and_navigation(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    home_page.click_my_account()
    home_page.click_login()
    expect(page).to_have_title(messages.LOGIN_PAGE_TITLE)
    expect(login_page.get_forgot_password()).to_be_visible()

    login_page.click_forgot_password()
    expect(page).to_have_title(messages.FORGOT_PASSWORD_PAGE_TITLE)
