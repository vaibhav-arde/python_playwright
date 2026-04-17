from pages.my_account_page import MyAccountPage
from playwright.sync_api import expect
import pytest
from pages.home_page import HomePage
from pages.logout_page import LogoutPage

@pytest.mark.ui
def test_user_logout(authenticated_page):

    page = authenticated_page
    
    page.goto(page.url.split("index.php")[0] + "index.php?route=account/account")

    my_account_page = MyAccountPage(page)
    home_page = HomePage(page)
    logout_page = LogoutPage(page)
    

    #Step 1: Open My Account dropdown
    my_account_page.click_my_account_dropdown()

    #Step 2: Click Logout
    my_account_page.click_logout()

    #Step 3: Verify Logout page using element
    expect(logout_page.btn_continue).to_be_visible()

    #Step 4: Click Continue
    logout_page.click_continue()

    #Step 5: Verify Home page using TITLE
    expect(page).to_have_title(home_page.get_home_page_title())