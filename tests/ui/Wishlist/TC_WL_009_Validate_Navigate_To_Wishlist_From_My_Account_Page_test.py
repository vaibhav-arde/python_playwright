import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.registration_page import RegistrationPage
from utils.constants import UIRoutes
from utils.messages import MY_WISHLIST_HEADING
from utils.random_test_data import RandomTestData


@pytest.mark.ui
def test_navigate_to_wishlist_from_my_account_page(page):
    home_page = HomePage(page)
    my_account_page = MyAccountPage(page)
    registration_page = RegistrationPage(page)

    # Pre-requisite: Create a fresh account to ensure a logged-in user state
    home_page.click_my_account()
    home_page.click_register()

    user_data = RandomTestData.get_user()
    registration_page.complete_registration(user_data)
    registration_page.click_continue()

    # Step 1: Click on 'Modify your wish list' option
    wishlist_page = my_account_page.click_modify_wishlist_option()

    # Validate ER-1: User should be taken to 'My Wish List' page
    expect(page).to_have_url(re.compile(rf".*{re.escape(UIRoutes.WISHLIST)}.*"))
    expect(wishlist_page.get_wishlist_page_heading()).to_have_text(MY_WISHLIST_HEADING)
