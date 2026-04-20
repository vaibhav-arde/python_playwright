import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.config import Config


@pytest.mark.sanity
def test_validate_the_text_into_the_Password_field_is_toggled_to_hide_its_visibility(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    # 1. Click on 'My Account' Dropmenu and navigate to Login page
    home_page.click_my_account()
    home_page.click_login()

    # 2. Enter any text into the 'Password' field (ER-1)
    login_page.get_password_field().fill(Config.invalid_password)

    # 3. Acceptance Criteria: Text entered into the Password field should be toggled to hide its visibility
    # This is verified by checking that the input field has type="password"
    expect(login_page.get_password_field()).to_have_attribute("type", "password")
