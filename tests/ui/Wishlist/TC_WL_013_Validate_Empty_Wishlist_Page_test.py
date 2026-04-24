import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.registration_page import RegistrationPage
from utils.constants import UIRoutes
from utils.messages import MY_ACCOUNT_HEADING, MY_WISHLIST_EMPTY_MESSAGE
from utils.random_test_data import RandomTestData


@pytest.mark.ui
def test_validate_empty_wishlist_page(page):
    home_page = HomePage(page)
    my_account_page = MyAccountPage(page)
    registration_page = RegistrationPage(page)

    # Pre-requisite: Create a fresh account to ensure a logged-in user with an empty wishlist
    home_page.click_my_account()
    home_page.click_register()

    user_data = RandomTestData.get_user()
    registration_page.complete_registration(user_data)
    registration_page.click_continue()

    # Step 1: Click on 'Modify your wish list' option
    wishlist_page = my_account_page.click_modify_wishlist_option()

    # Validate ER-1: Empty wishlist message should be displayed
    expect(wishlist_page.get_empty_wishlist_message()).to_have_text(MY_WISHLIST_EMPTY_MESSAGE)

    # Step 2: Click on 'Continue' button
    my_account_page = wishlist_page.click_continue_button()

    # Validate ER-2: User should be taken to 'My Account' page
    expect(page).to_have_url(re.compile(rf".*{re.escape(UIRoutes.MY_ACCOUNT)}.*"))
    expect(my_account_page.get_my_account_page_heading()).to_have_text(MY_ACCOUNT_HEADING)
