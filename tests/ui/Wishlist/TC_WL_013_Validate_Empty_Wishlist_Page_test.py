import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from utils.constants import UIRoutes
from utils.messages import MY_ACCOUNT_HEADING, MY_WISHLIST_EMPTY_MESSAGE


@pytest.mark.ui
def test_validate_empty_wishlist_page(authenticated_page):
    home_page = HomePage(authenticated_page)
    my_account_page = MyAccountPage(authenticated_page)

    home_page.click_my_account()
    home_page.click_my_account_option()

    # Step 1: Click on 'Modify your wish list' option
    wishlist_page = my_account_page.click_modify_wishlist_option()

    # Clear wishlist if it has items
    try:
        while wishlist_page.wishlist_rows.count() > 0:
            wishlist_page.wishlist_rows.first.locator("a[data-original-title='Remove']").click()
            wishlist_page.page.wait_for_load_state("networkidle")
    except Exception:
        pass

    # Validate ER-1: Empty wishlist message should be displayed
    # NOTE: This assumes the authenticated user has an empty wishlist.
    expect(wishlist_page.get_empty_wishlist_message()).to_have_text(MY_WISHLIST_EMPTY_MESSAGE)

    # Step 2: Click on 'Continue' button
    my_account_page = wishlist_page.click_continue_button()

    # Validate ER-2: User should be taken to 'My Account' page
    expect(authenticated_page).to_have_url(re.compile(rf".*{re.escape(UIRoutes.MY_ACCOUNT)}.*"))
    expect(my_account_page.get_my_account_page_heading()).to_have_text(MY_ACCOUNT_HEADING)
