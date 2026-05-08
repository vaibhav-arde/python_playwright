import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from pages.search_results_page import SearchResultsPage
from pages.wishlist_page import WishListPage
from pages.shopping_cart_page import ShoppingCartPage
from utils.constants import TestData
from utils.messages import PDP_ADD_TO_CART_SUCCESS_PREFIX, PDP_ADD_TO_CART_SUCCESS_SUFFIX
from utils.random_test_data import RandomTestData


@pytest.mark.regression
@pytest.mark.ui
def test_atc_002_validate_adding_product_to_cart_from_wishlist(page):
    """
    Test Steps:
    1. Click on 'Wish List' header option
    2. Click on 'Add to Cart' icon option in the displayed 'My Wish List' page (Validate ER-1)
    3. Click on 'Shopping Cart' header option (Validate ER-2)
    """

    # Page Objects Initialization
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)
    search_results_page = SearchResultsPage(page)
    wishlist_page = WishListPage(page)
    shopping_cart_page = ShoppingCartPage(page)

    # Pre-requisite 1: Register a new account to ensure active session
    home_page.click_my_account()
    home_page.click_register()

    unique_user = RandomTestData.get_user()
    registration_page.complete_registration(unique_user)
    expect(registration_page.get_confirmation_msg()).to_be_visible()

    # Pre-requisite 2: A product is added to Wish List page
    home_page.enter_product_name(TestData.PRODUCT_NAME_IMAC)
    home_page.click_search()
    product_page = search_results_page.select_product(TestData.PRODUCT_NAME_IMAC)
    product_page.click_add_to_wishlist()

    # Step 1: Click on 'Wish List' header option
    home_page.click_wishlist()

    # Step 2: Click on 'Add to Cart' icon option in the displayed 'My Wish List' page
    wishlist_page.click_add_to_cart(TestData.PRODUCT_NAME_IMAC)

    # Validate ER-1: Success message with text - 'Success: You have added Product Name to your shopping cart!' should be displayed
    expected_success_msg = f"{PDP_ADD_TO_CART_SUCCESS_PREFIX} {TestData.PRODUCT_NAME_IMAC} {PDP_ADD_TO_CART_SUCCESS_SUFFIX}"
    expect(wishlist_page.get_confirmation_message()).to_contain_text(expected_success_msg)

    # Step 3: Click on 'Shopping Cart' header option
    home_page.click_shopping_cart()

    # Validate ER-2: Product should be successfully displayed in the 'Shopping Cart' page
    expect(shopping_cart_page.get_product_row_by_name(TestData.PRODUCT_NAME_IMAC)).to_be_visible()
