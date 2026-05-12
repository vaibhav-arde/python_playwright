import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from utils.constants import BreadcrumbOptionNames, UIRoutes
from utils.messages import MY_ACCOUNT_HEADING, MY_WISHLIST_HEADING


@pytest.mark.ui
def test_validate_breadcrumb_in_wishlist_page(authenticated_page):
    home_page = HomePage(authenticated_page)
    my_account_page = MyAccountPage(authenticated_page)

    home_page.click_my_account()
    home_page.click_my_account_option()

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
    expect(authenticated_page).to_have_url(re.compile(rf".*{re.escape(UIRoutes.MY_ACCOUNT)}.*"))
    expect(my_account_page.get_my_account_page_heading()).to_have_text(MY_ACCOUNT_HEADING)

    wishlist_page = my_account_page.click_modify_wishlist_option()
    expect(authenticated_page).to_have_url(re.compile(rf".*{re.escape(UIRoutes.WISHLIST)}.*"))
    expect(wishlist_page.get_wishlist_page_heading()).to_have_text(MY_WISHLIST_HEADING)

    home_page = wishlist_page.click_home_breadcrumb()
    expect(authenticated_page).to_have_url(re.compile(rf".*{re.escape(UIRoutes.COMMON_HOME)}.*"))
