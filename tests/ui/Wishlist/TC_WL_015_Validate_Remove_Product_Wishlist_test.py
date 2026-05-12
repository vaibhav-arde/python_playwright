import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.search_results_page import SearchResultsPage
from utils.messages import (
    ERR_PRODUCT_NOT_FOUND,
    SUCCESS_WISH_LIST_MODIFIED,
    MY_WISHLIST_EMPTY_MESSAGE,
)
from utils.constants import TestData


@pytest.mark.ui
@pytest.mark.critical
def test_validate_remove_product_wishlist_page(authenticated_page):
    """
    TC_WL_015: Validate the removing the Product from 'My Wish List' page
    """
    home_page = HomePage(authenticated_page)
    my_account_page = MyAccountPage(authenticated_page)
    search_results_page = SearchResultsPage(authenticated_page)

    # Clear wishlist first to ensure it will be empty after we remove our product
    home_page.click_my_account()
    home_page.click_my_account_option()
    wishlist_page = my_account_page.click_modify_wishlist_option()
    try:
        while wishlist_page.wishlist_rows.count() > 0:
            wishlist_page.wishlist_rows.first.locator("a[data-original-title='Remove']").click()
            wishlist_page.page.wait_for_load_state("networkidle")
    except Exception:
        pass

    # Pre-requisite: One product is added to 'My Wish List' page
    product_name = TestData.PRODUCT_IMAC
    home_page.click_logo()
    home_page.enter_product_name(product_name)
    home_page.click_search()
    product_page = search_results_page.select_product(product_name)
    assert product_page is not None, ERR_PRODUCT_NOT_FOUND.format(product_name=product_name)

    product_page.add_product_to_wishlist()
    expect(product_page.get_confirmation_message()).to_be_visible()

    # Navigate to My Account
    home_page.click_my_account()
    home_page.click_my_account_option()

    # Test Step 1: Click on 'Modify your wish list' option
    wishlist_page = my_account_page.click_modify_wishlist_option()

    # Test Step 2: Click on 'Remove' icon option
    wishlist_page.remove_product(product_name)

    # Acceptance Criteria:
    # 1. Success message with text - 'Success: You have modified your wish list!' should be displayed
    expect(wishlist_page.get_success_message()).to_contain_text(SUCCESS_WISH_LIST_MODIFIED)

    # 2. 'My Wish List' page should become empty and 'Your wish list is empty.' text should be displayed
    expect(wishlist_page.get_empty_wishlist_message()).to_have_text(MY_WISHLIST_EMPTY_MESSAGE)
