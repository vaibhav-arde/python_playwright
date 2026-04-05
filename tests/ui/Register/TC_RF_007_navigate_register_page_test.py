"""
1. Click on 'My Account' Drop menu
2. Click on 'Register' option (ER-1)

3. Click on 'My Account' Drop menu
4. Click on 'Login' option
5. Click on 'Continue' button inside 'New Customer' box (ER-1)

6. Repeat Steps 3 and 4
7. Click on 'Register' option from the Right Column options (ER-1)
"""

import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from utils.constants import UILabels


@pytest.mark.sanity
def test_navigation_to_register_page(page):

    home_page = HomePage(page)
    login_page = LoginPage(page)
    registration_page = RegistrationPage(page)

    # ---- Path 1: My Account → Register ----
    home_page.click_my_account()
    home_page.click_register()

    expect(registration_page.lbl_page_heading).to_have_text(UILabels.REGISTER_PAGE_HEADING)
    
    # ---- Path 2: My Account → Login → Continue ----
    # Reset
    page.goto("")
    home_page.click_my_account()
    home_page.click_login()

    login_page.click_continue()

    expect(registration_page.lbl_page_heading).to_have_text(UILabels.REGISTER_PAGE_HEADING)

    # ---- Path 3: Login → Right Column Register ----
    # Reset
    page.goto("")
    home_page.click_my_account()
    home_page.click_login()
    login_page.click_right_column_register()

    expect(registration_page.lbl_page_heading).to_have_text(UILabels.REGISTER_PAGE_HEADING)
