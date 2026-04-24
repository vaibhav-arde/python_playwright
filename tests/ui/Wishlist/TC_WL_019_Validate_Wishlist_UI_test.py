import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.registration_page import RegistrationPage
from pages.search_results_page import SearchResultsPage
from utils.messages import (
    ERR_PRODUCT_NOT_FOUND,
    MY_WISHLIST_HEADING,
    MY_WISHLIST_EMPTY_MESSAGE,
    ERR_WISHLIST_HEADERS_MISMATCH,
)
from utils.constants import TestData, WishlistColumnNames
from utils.random_test_data import RandomTestData


@pytest.mark.ui
def test_validate_wishlist_ui(page):
    """
    TC_WL_019: Validate the UI of 'Wish List' functionality
    """
    home_page = HomePage(page)
    my_account_page = MyAccountPage(page)
    registration_page = RegistrationPage(page)
    search_results_page = SearchResultsPage(page)

    # Pre-requisite: Create a fresh account
    home_page.click_my_account()
    home_page.click_register()
    user_data = RandomTestData.get_user()
    registration_page.complete_registration(user_data)
    registration_page.click_continue()

    # Navigate to Wishlist (Empty state)
    wishlist_page = my_account_page.click_wishlist_right_column_option()

    # Validate UI for Empty Wishlist
    expect(wishlist_page.get_wishlist_page_heading()).to_have_text(MY_WISHLIST_HEADING)
    expect(wishlist_page.get_empty_wishlist_message()).to_have_text(MY_WISHLIST_EMPTY_MESSAGE)
    expect(wishlist_page.get_continue_button()).to_be_visible()
    expect(wishlist_page.get_home_breadcrumb_link()).to_be_visible()
    expect(wishlist_page.get_account_breadcrumb_link()).to_be_visible()
    expect(wishlist_page.get_wishlist_breadcrumb_link()).to_be_visible()

    # Add a product to Wishlist to check table UI
    product_name = TestData.PRODUCT_IMAC
    home_page.click_logo()
    home_page.enter_product_name(product_name)
    home_page.click_search()
    product_page = search_results_page.select_product(product_name)
    assert product_page is not None, ERR_PRODUCT_NOT_FOUND.format(product_name=product_name)

    product_page.add_product_to_wishlist()
    expect(product_page.get_confirmation_message()).to_be_visible()

    # Navigate back to Wishlist (Populated state)
    wishlist_page = product_page.click_wishlist_link_in_message()

    # Validate Table UI and Columns
    expected_headers = [
        WishlistColumnNames.IMAGE,
        WishlistColumnNames.PRODUCT_NAME,
        WishlistColumnNames.MODEL,
        WishlistColumnNames.STOCK,
        WishlistColumnNames.UNIT_PRICE,
        WishlistColumnNames.ACTION,
    ]
    assert (
        wishlist_page.get_wishlist_table_headers() == expected_headers
    ), ERR_WISHLIST_HEADERS_MISMATCH.format(
        expected=expected_headers, actual=wishlist_page.get_wishlist_table_headers()
    )

    # Validate row elements visibility for the product
    expect(wishlist_page.get_product_image_link(product_name)).to_be_visible()
    expect(wishlist_page.get_product_name_link(product_name)).to_be_visible()
    expect(wishlist_page.get_product_model(product_name)).to_be_visible()
    expect(wishlist_page.get_product_stock(product_name)).to_be_visible()
    expect(wishlist_page.get_product_unit_price(product_name)).to_be_visible()
    expect(wishlist_page.get_add_to_cart_button(product_name)).to_be_visible()
    expect(wishlist_page.get_remove_link(product_name)).to_be_visible()
