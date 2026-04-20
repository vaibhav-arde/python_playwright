import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from utils.config import Config
from utils import messages


@pytest.mark.sanity
def test_login_using_keyboard_keys(page, registered_user): 
    home_page = HomePage(page)
    login_page = LoginPage(page)

    # 1. Click on 'My Account' Dropmenu
    home_page.click_my_account()
    
    # 2. Click on 'Login' option
    home_page.click_login()
    expect(page).to_have_title(messages.LOGIN_PAGE_TITLE, timeout=5000)

    # 3. Perform login using keyboard interactions (refactored to POM)
    login_page.login_with_keyboard(registered_user['email'], registered_user['password'])

    # (ER-1) Verify navigation to My Account page
    expect(page).to_have_title(messages.ACCOUNT_PAGE_TITLE, timeout=10000)
    my_account_page = MyAccountPage(page)
    expect(my_account_page.get_my_account_page_heading()).to_be_visible()
