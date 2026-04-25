import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils import messages


@pytest.mark.ui
def test_empty_credentials_login(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    home_page.click_my_account()
    home_page.click_login()

    login_page.login(messages.EMPTY_FIELDS, messages.EMPTY_FIELDS)

    expect(login_page.get_login_error()).to_be_visible()
