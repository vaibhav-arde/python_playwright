import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from utils.config import Config


@pytest.mark.sanity
def test_invalid_password_login(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    home_page.click_my_account()
    home_page.click_login()

    login_page.login(Config.email, Config.invalid_password)

    expect(login_page.get_login_error()).to_be_visible(timeout=5000)