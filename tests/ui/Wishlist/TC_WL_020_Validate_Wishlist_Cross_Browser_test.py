import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from pages.search_results_page import SearchResultsPage
from utils.messages import (
    ERR_PRODUCT_NOT_FOUND,
    SUCCESS_ADD_TO_CART,
    SUCCESS_WISH_LIST_MODIFIED,
    MY_WISHLIST_EMPTY_MESSAGE,
)
from utils.constants import TestData
from utils.random_test_data import RandomTestData


@pytest.mark.ui
@pytest.mark.cross_browser
def test_validate_wishlist_functionality_e2e(page):
    """
    TC_WL_020: Validate the 'Wish List' functionality in all the supported environments
    This test covers the core lifecycle of a wishlist item.
    """
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)
    search_results_page = SearchResultsPage(page)

    # 1. Setup: Create a fresh account
    home_page.click_my_account()
    home_page.click_register()
    user_data = RandomTestData.get_user()
    registration_page.complete_registration(user_data)
    registration_page.click_continue()

    # 2. Add product to wishlist
    product_name = TestData.PRODUCT_IMAC
    home_page.click_logo()
    home_page.enter_product_name(product_name)
    home_page.click_search()
    product_page = search_results_page.select_product(product_name)
    assert product_page is not None, ERR_PRODUCT_NOT_FOUND.format(product_name=product_name)

    product_page.add_product_to_wishlist()
    expect(product_page.get_confirmation_message()).to_be_visible()

    # 3. Navigate to Wishlist and verify product
    wishlist_page = product_page.click_wishlist_link_in_message()
    expect(wishlist_page.is_product_in_wishlist(product_name)).to_be_visible()

    # 4. Add to cart from wishlist
    wishlist_page.add_product_to_cart(product_name)
    expected_cart_msg = SUCCESS_ADD_TO_CART.format(product_name=product_name)
    expect(wishlist_page.get_success_message()).to_contain_text(expected_cart_msg)

    # 5. Remove from wishlist
    wishlist_page.remove_product(product_name)
    expect(wishlist_page.get_success_message()).to_contain_text(SUCCESS_WISH_LIST_MODIFIED)

    # 6. Verify wishlist is empty
    expect(wishlist_page.get_empty_wishlist_message()).to_have_text(MY_WISHLIST_EMPTY_MESSAGE)
