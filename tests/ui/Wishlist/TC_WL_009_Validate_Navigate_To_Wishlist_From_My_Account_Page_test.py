import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from utils.constants import UIRoutes
from utils.messages import MY_WISHLIST_HEADING


@pytest.mark.ui
def test_navigate_to_wishlist_from_my_account_page(authenticated_page):
    home_page = HomePage(authenticated_page)
    my_account_page = MyAccountPage(authenticated_page)

    home_page.click_my_account()
    home_page.click_my_account_option()

    # Step 1: Click on 'Modify your wish list' option
    wishlist_page = my_account_page.click_modify_wishlist_option()

    # Validate ER-1: User should be taken to 'My Wish List' page
    expect(authenticated_page).to_have_url(re.compile(rf".*{re.escape(UIRoutes.WISHLIST)}.*"))
    expect(wishlist_page.get_wishlist_page_heading()).to_have_text(MY_WISHLIST_HEADING)
