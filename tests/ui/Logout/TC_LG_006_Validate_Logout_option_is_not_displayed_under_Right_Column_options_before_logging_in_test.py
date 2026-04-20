from playwright.sync_api import expect
import pytest
from pages.home_page import HomePage

@pytest.mark.ui
def test_logout_not_visible_without_login(page):

    # Open application URL
    home_page = HomePage(page)

    # Step 1: Click My Account dropdown
    home_page.click_my_account()

    # Step 2: Click Register
    home_page.click_register()

    # Initialize MyAccountPage to evaluate the right-column generic navigation sidebar
    from pages.my_account_page import MyAccountPage
    my_account_page = MyAccountPage(page)

    # Step 3: Verify logout option should not be displayed Right Column
    expect(my_account_page.verify_logout_sidebar_visible()).to_be_hidden()