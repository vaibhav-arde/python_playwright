from pages.my_account_page import MyAccountPage
from playwright.sync_api import expect
import pytest
from pages.logout_page import LogoutPage
from pages.login_page import LoginPage


@pytest.mark.ui
def test_user_logout(authenticated_page):

    page = authenticated_page
    base_url = page.url.split("index.php")[0]

    my_account_page = MyAccountPage(page)
    logout_page = LogoutPage(page)
    login_page = LoginPage(page)

    my_account_page.open_my_account_page(base_url)

    # Step 1: Verify Login page using TITLE
    expect(page).to_have_title(my_account_page.get_expected_title())

    # Step 2: Click My Account dropdown
    my_account_page.click_my_account_dropdown()

    # Step 3: Click Logout
    my_account_page.click_logout()

    # Step 4: Verify Logout page
    expect(logout_page.verify_logout_page_heading()).to_be_visible()

    # Step 5: Click Browser Back button
    my_account_page.go_back()

    # Step 6: Click Subscribe / unsubscribe to newsletter
    my_account_page.click_newsletter_subscription()

    # Step 7: Verify Login page display
    expect(login_page.verify_login_btn_visible()).to_be_visible()
