"""
1. Click on 'My Account' dropdown
2. Select 'My Account' option
3. Click on 'Edit your account information' link on the displayed 'My Account' page
4. Update all the details in the fields - First Name, Last Name, E-Mail and Telephone
5. Click on 'Continue' button (Validate ER-1 and ER-2)
6. Logout and login with new updated Email Address (Validate ER-3)
7. Logout and login with old Email Address (Validate ER-4)
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from pages.edit_account_page import EditAccountPage
from utils.constants import UIRoutes
from utils.random_test_data import RandomTestData, update_registered_user


@pytest.mark.ui
@pytest.mark.critical
def test_update_my_account_information_successfully(page, registered_user):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    my_account_page = MyAccountPage(page)
    edit_account_page = EditAccountPage(page)

    home_page.click_my_account()
    home_page.click_login()

    login_page.login_user(registered_user)
    expect(my_account_page.get_my_account_page_heading()).to_be_visible()
    home_page.click_my_account()
    home_page.click_my_account_option()
    my_account_page.click_edit_account_info()

    expect(edit_account_page.get_page_heading()).to_be_visible()
    expect(page).to_have_url(UIRoutes.EDIT_ACCOUNT_INFORMATION)

    # ===== Step 3: Update Details =====
    updated_user = RandomTestData.get_user()

    edit_account_page.update_account_information(updated_user)
    edit_account_page.click_continue()

    # ===== Step 4: Validate Success Message =====
    expect(edit_account_page.get_success_message()).to_be_visible()

    # ===== Step 5: Logout =====
    my_account_page.click_logout()

    # ===== Step 6: Login with new email =====
    home_page.click_my_account()
    home_page.click_login()
    login_page.login(updated_user["email"], registered_user["password"])

    expect(my_account_page.get_my_account_page_heading()).to_be_visible()

    # ===== Step 7: Negative validation (old email) =====
    my_account_page.click_logout()

    home_page.click_my_account()
    home_page.click_login()
    login_page.login_user(registered_user)

    expect(login_page.get_login_error()).to_be_visible()

    # ===== Update the globally shared cached user so future tests don't fail =====
    update_registered_user(registered_user, updated_user)
