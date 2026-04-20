from pages.my_account_page import MyAccountPage
from playwright.sync_api import expect
import pytest
from pages.home_page import HomePage
from pages.logout_page import LogoutPage

@pytest.mark.ui
def test_user_logout(authenticated_page):

    page = authenticated_page
    base_url = page.url.split("index.php")[0]

    my_account_page = MyAccountPage(page)
    home_page = HomePage(page)
    logout_page = LogoutPage(page)
    
    my_account_page.open_my_account_page(base_url)
    

    #Step 1: Open My Account dropdown
    my_account_page.click_my_account_dropdown()

    #Step 2: Click Logout
    my_account_page.click_logout()

    #Step 3: Verify Logout page using element
    expect(logout_page.verify_logout_page_heading()).to_be_visible()

    #Step 4: Click dropdown menu from logout page
    logout_page.click_dropdown_logout_page()

    #Step 5: Verify Login button is visible
    expect(logout_page.verify_login_btn_in_dropdown()).to_be_visible()

    #Step 6: Click Continue
    logout_page.click_continue()

    #Step 7: Verify Home page using TITLE
    expect(page).to_have_title(home_page.get_expected_title())