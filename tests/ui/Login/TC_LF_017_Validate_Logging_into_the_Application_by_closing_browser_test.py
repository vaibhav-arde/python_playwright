import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.config import Config


@pytest.mark.ui
def test_validate_logging_into_the_application_by_closing_browser(context, base_url):
    # Use the context provided by pytest-playwright directly.
    # In headed mode, pytest-playwright creates one default page.
    # We close it first to avoid having an unused empty tab.
    pages = context.pages
    for p in pages:
        p.close()

    page = context.new_page()
    home_page = HomePage(page)
    login_page = LoginPage(page)

    # 1. Click on 'My Account' Dropmenu and navigate to Login page
    page.goto(base_url)
    home_page.click_my_account()
    home_page.click_login()

    # 2. Enter valid email address and password
    # Using UserDetails from constants as per test data requirements
    login_page.login(Config.email, Config.password)

    # 3. Close the Browser (Close the page)
    page.close()

    # 4. Open the Browser and open the Application URL
    page = context.new_page()
    home_page = HomePage(page)
    page.goto(base_url)

    # 5. Validate Loggedin Session should be still maintained
    home_page.click_my_account()
    expect(home_page.logout_link()).to_be_visible()
