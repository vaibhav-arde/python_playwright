from pages import my_account_page
from playwright.sync_api import expect
import pytest
from pages.home_page import HomePage
from pages.logout_page import LogoutPage
from pages.my_account_page import MyAccountPage


@pytest.mark.ui
@pytest.mark.logout
def test_user_logout(authenticated_page):

    page = authenticated_page
    
    page.goto(page.url.split("index.php")[0] + "index.php?route=account/account")

    home_page = HomePage(page)
    my_account_page = MyAccountPage(page)
    logout_page = LogoutPage(page)

    #Step 1: Verify logout option
    expect(my_account_page.lnk_logout_sidebar).to_be_visible()

    #Step 2: Click logout
    my_account_page.click_logout_sidebar()

    #Step 3: Verify logout page
    logout_page.verify_logout_page()

    #Step 4: Click continue
    logout_page.click_continue()

    #Step 5: Verify home page
    expect(page).to_have_title(home_page.get_home_page_title())

    #Step 6: Verify login visible
    home_page.verify_login_visible_after_logout()