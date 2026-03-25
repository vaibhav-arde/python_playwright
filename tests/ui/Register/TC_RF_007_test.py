import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage


@pytest.fixture
def page(browser):
    """
    Override the default page fixture to ensure clean navigation to
    opencart.abstracta.us and avoid chromewebdata / connection errors.
    """
    context = browser.new_context(ignore_https_errors=True)
    p = context.new_page()
    p.goto("http://opencart.abstracta.us/", wait_until="domcontentloaded")
    yield p
    context.close()

@pytest.fixture(scope="function", autouse=True)
def navigate_to_base_url():
    """
    Override global fixture to completely disable automatic navigation.
    We handle navigation locally in the custom page fixture instead.
    """
    pass


@pytest.mark.sanity
@pytest.mark.regression
def test_navigate_to_register_page(page: Page):
    """
    Validate different ways of navigating to 'Register Account' page
    """
    home_page = HomePage(page)

    # 1. Open the Application (Handled by fixture above)

    # 2. Click on 'My Account' Drop menu
    home_page.click_my_account()
    
    # 3. Click on 'Register' option (ER-1)
    home_page.click_register()
    expect(page).to_have_title("Register Account")

    # 4. Click on 'My Account' Drop menu
    home_page.click_my_account()
    
    # 5. Click on 'Login' option
    page.locator("#top-links a:has-text('Login')").click()
    
    # 6. Click on 'Continue' button inside 'New Customer' box (ER-1)
    page.locator("a.btn-primary:has-text('Continue')").click()
    expect(page).to_have_title("Register Account")

    # 7. Repeat Steps 4 and 5 (which means clicking My Account -> Login)
    home_page.click_my_account()
    page.locator("#top-links a:has-text('Login')").click()

    # 8. Click on 'Register' option from the Right Column options (ER-1)
    page.locator("a.list-group-item:has-text('Register')").click()
    expect(page).to_have_title("Register Account")
