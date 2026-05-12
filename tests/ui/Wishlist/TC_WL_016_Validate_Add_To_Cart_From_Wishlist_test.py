import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.search_results_page import SearchResultsPage
from utils.messages import (
    ERR_PRODUCT_NOT_FOUND,
    SUCCESS_ADD_TO_CART,
)
from utils.constants import TestData


@pytest.mark.ui
@pytest.mark.critical
def test_validate_add_to_cart_from_wishlist_page(authenticated_page):
    """
    TC_WL_016: Validate adding the product to Cart from the 'My Wish List' page
    """
    home_page = HomePage(authenticated_page)
    my_account_page = MyAccountPage(authenticated_page)
    search_results_page = SearchResultsPage(authenticated_page)

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

    # Test Step 2: Click on 'Add to Cart' icon option
    wishlist_page.add_product_to_cart(product_name)

    # Acceptance Criteria:
    # 1. Success message with text - 'Success: You have added Product Name to your shopping cart!' should be displayed
    expected_msg = SUCCESS_ADD_TO_CART.format(product_name=product_name)
    expect(wishlist_page.get_success_message()).to_contain_text(expected_msg)
