import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.config import Config


@pytest.mark.xfail
@pytest.mark.sanity
def test_validate_unsuccessful_login_attempts(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    # 1. Click on 'My Account' Dropmenu and navigate to Login page
    home_page.click_my_account()
    home_page.click_login()

    # Repeat steps 3 to 5: enter invalid credentials and click login (total 5 times)
    for i in range(5):
        # Enter invalid email and password, then click login
        login_page.login(Config.invalid_email, Config.invalid_password)
        
        # 5th attempt (i == 4) should show the exceeded attempts warning
        if i == 4:
            expect(login_page.get_login_attempts_error()).to_be_visible(timeout=5000)
        else:
            # First 4 attempts should show the standard login error
            expect(login_page.get_login_error()).to_be_visible(timeout=5000)
