import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from utils.constants import UIRoutes
from utils.messages import MY_WISHLIST_HEADING, MY_WISHLIST_PAGE_TITLE


@pytest.mark.ui
def test_validate_page_title_page_url_and_page_heading_of_wishlist_page(authenticated_page):
    home_page = HomePage(authenticated_page)
    my_account_page = MyAccountPage(authenticated_page)

    # Navigate to My Account page where the 'Modify your wish list' option is visible
    home_page.click_my_account()
    home_page.click_my_account_option()

    # Step 1: Click on 'Modify your wish list' option
    wishlist_page = my_account_page.click_modify_wishlist_option()

    # Step 2: Check the Page Title, Page URL and Page Heading
    expect(authenticated_page).to_have_title(MY_WISHLIST_PAGE_TITLE)
    expect(authenticated_page).to_have_url(re.compile(rf".*{re.escape(UIRoutes.WISHLIST)}.*"))
    expect(wishlist_page.get_wishlist_page_heading()).to_have_text(MY_WISHLIST_HEADING)
