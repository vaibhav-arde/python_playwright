from playwright.sync_api import expect
import pytest
from pages.home_page import HomePage

@pytest.mark.ui
def test_logout_not_visible_without_login(page):

    # Open application URL
    home_page = HomePage(page)

    # Step 1: Click My Account dropdown
    home_page.click_my_account()

    # Step 2: Verify Logout button is not visible
    expect(home_page.verify_logout_btn()).not_to_be_visible()
