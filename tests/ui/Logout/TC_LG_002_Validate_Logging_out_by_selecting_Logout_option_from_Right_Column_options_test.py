from pages import my_account_page
from playwright.sync_api import expect
import pytest
from pages.home_page import HomePage
from pages.logout_page import LogoutPage
from pages.my_account_page import MyAccountPage


@pytest.mark.ui
def test_user_logout(authenticated_page):

    page = authenticated_page
    
    page.goto(page.url.split("index.php")[0] + "index.php?route=account/account")

    home_page = HomePage(page)
    my_account_page = MyAccountPage(page)
    logout_page = LogoutPage(page)

    #Step 1: Click logout from right column
    my_account_page.click_logout_sidebar()

    #Step 2: Verify logout page
    expect(logout_page.verify_logout_page_heading()).to_have_text("Account Logout")

    #Step 3: Click dropdown menu from logout page
    logout_page.click_dropdown_logout_page()

    #Step 4: Verify Login button is visible
    expect(logout_page.verify_login_btn_in_dropdown()).to_be_visible()

    #Step 5: Click continue
    logout_page.click_continue()

    #Step 6: Verify home page
    expect(page).to_have_title(home_page.get_home_page_title())