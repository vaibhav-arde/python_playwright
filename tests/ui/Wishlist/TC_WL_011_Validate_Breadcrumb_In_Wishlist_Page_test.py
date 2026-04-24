import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.registration_page import RegistrationPage
from utils.constants import BreadcrumbOptionNames, UIRoutes
from utils.messages import MY_ACCOUNT_HEADING, MY_WISHLIST_HEADING
from utils.random_test_data import RandomTestData


@pytest.mark.ui
def test_validate_breadcrumb_in_wishlist_page(page):
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

    # Step 2: Check the breadcrumb displayed in the 'Wish List' page
    expect(wishlist_page.get_home_breadcrumb_link()).to_be_visible()
    expect(wishlist_page.get_account_breadcrumb_link()).to_have_text(BreadcrumbOptionNames.ACCOUNT)
    expect(wishlist_page.get_wishlist_breadcrumb_link()).to_have_text(
        BreadcrumbOptionNames.MY_WISH_LIST
    )

    # Validate ER-1: Breadcrumb should be displayed correctly and work correctly
    my_account_page = wishlist_page.click_account_breadcrumb()
    expect(page).to_have_url(re.compile(rf".*{re.escape(UIRoutes.MY_ACCOUNT)}.*"))
    expect(my_account_page.get_my_account_page_heading()).to_have_text(MY_ACCOUNT_HEADING)

    wishlist_page = my_account_page.click_modify_wishlist_option()
    expect(page).to_have_url(re.compile(rf".*{re.escape(UIRoutes.WISHLIST)}.*"))
    expect(wishlist_page.get_wishlist_page_heading()).to_have_text(MY_WISHLIST_HEADING)

    home_page = wishlist_page.click_home_breadcrumb()
    expect(page).to_have_url(re.compile(rf".*{re.escape(UIRoutes.COMMON_HOME)}.*"))
