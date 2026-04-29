import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from pages.shopping_cart_page import ShoppingCartPage
from utils.constants import TestData
from utils.messages import PDP_ADD_TO_CART_SUCCESS_PREFIX, PDP_ADD_TO_CART_SUCCESS_SUFFIX


@pytest.mark.regression
@pytest.mark.ui
def test_atc_004_validate_adding_product_to_cart_from_related_products_section(page):
    """
    [TASK] TC_ATC_004 Validate adding the product to Cart from_Related_Products_section of the Product Display Page

    Test Steps:
    1. Enter any existing Product name into the Search text box field - Apple Cinema 30"
    2. Click on the button having search icon
    3. Click on the Product displayed in the Search results
    4. Click on 'Add to Cart' button on one of the Products displayed in the Related Products section (Validate ER-1)
    5. Click on the 'shopping cart!' link in the displayed success message (Validate ER-2)
    """

    # Page Objects Initialization
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)
    shopping_cart_page = ShoppingCartPage(page)

    # Step 1: Enter any existing Product name into the Search text box field
    home_page.enter_product_name(TestData.PRODUCT_NAME_APPLE_CINEMA_30)

    # Step 2: Click on the button having search icon
    home_page.click_search()

    # Step 3: Click on the Product displayed in the Search results
    search_results_page.select_product(TestData.PRODUCT_NAME_APPLE_CINEMA_30)

    # Pre-step: Get the name of the first related product to use in validation
    # If no related products exist, this test should fail or skip, but we assume it exists for Apple Cinema 30"
    related_product_name = product_page.get_related_product_name(0)

    # Step 4: Click on 'Add to Cart' button on one of the Products displayed in the Related Products section
    product_page.click_add_to_cart_for_related_product(related_product_name)

    # Validate ER-1: Success message with text - 'Success: You have added Product Name to your shopping cart!' should be displayed
    expected_success_msg = f"{PDP_ADD_TO_CART_SUCCESS_PREFIX} {related_product_name} {PDP_ADD_TO_CART_SUCCESS_SUFFIX}"
    expect(product_page.get_confirmation_message()).to_contain_text(expected_success_msg)

    # Step 5: Click on the 'shopping cart!' link in the displayed success message
    product_page.click_shopping_cart_link()

    # Validate ER-2: Product should be successfully displayed in the 'Shopping Cart' page
    expect(shopping_cart_page.get_product_row_by_name(related_product_name)).to_be_visible()
