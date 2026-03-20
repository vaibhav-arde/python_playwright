import pytest
from playwright.sync_api import Page, expect

# Direct - inject userlogin with url

# https://the-internet.herokuapp.com/basic_auth
# https://the-internet.herokuapp.com/basic_auth
# https://admin:admin@the-internet.herokuapp.com/basic_auth


@pytest.mark.skip
def test_authPopup(page: Page):
    page.goto("https://admin:admin@the-internet.herokuapp.com/basic_auth")
    page.wait_for_load_state()
    expect(page.locator("text=Congratulations")).to_be_visible()
    page.wait_for_timeout(5000)


# using context - we can pass user and password along with the context
# def test_authPopup_context(playwright:Playwright):
#     browser=playwright.chromium.launch(headless=False)
#     context=browser.new_context(
#         http_credentials={"username":"admin","password":"admin"}
#     )
#     page=context.new_page()
# To keep pytest-playwright video/tracing features intact, we override browser_context_args
@pytest.fixture
def browser_context_args(browser_context_args):
    return {**browser_context_args, "http_credentials": {"username": "admin", "password": "admin"}}


def test_authPopup_context(page: Page):
    page.goto("https://the-internet.herokuapp.com/basic_auth")
    page.wait_for_load_state()
    expect(page.locator("text=Congratulations Test")).to_be_visible()
    page.wait_for_timeout(5000)
