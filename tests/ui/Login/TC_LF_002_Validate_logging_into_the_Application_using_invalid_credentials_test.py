import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.config import Config


@pytest.mark.ui
def test_invalid_user_login(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    home_page.click_my_account()
    home_page.click_login()

    login_page.login(Config.invalid_email, Config.invalid_password)

    expect(login_page.get_login_error()).to_be_visible()
