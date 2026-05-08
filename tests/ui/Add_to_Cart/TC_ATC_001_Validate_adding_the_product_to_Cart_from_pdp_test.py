import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.constants import TestData
from utils.messages import PDP_ADD_TO_CART_SUCCESS_PREFIX, PDP_ADD_TO_CART_SUCCESS_SUFFIX


@pytest.mark.critical
@pytest.mark.regression
@pytest.mark.ui
def test_atc_001_validate_adding_product_to_cart_from_pdp(page):
    """
    Test Steps:
    1. Enter any existing Product name into the Search text box field - iMac
    2. Click on the button having search icon
    3. Click on the Product displayed in the Search results
    4. Click on 'Add to Cart' button in the displayed 'Product Display' page (Validate ER-1)
    5. Click on the 'shopping_cart!' link in the displayed success message (Validate ER-2)
    """

    # Page Objects Initialization
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    # Step 1: Enter any existing Product name into the Search text box field
    home_page.enter_product_name(TestData.PRODUCT_NAME_IMAC)

    # Step 2: Click on the button having search icon
    home_page.click_search()

    # Step 3: Click on the Product displayed in the Search results
    product_page = search_results_page.select_product(TestData.PRODUCT_NAME_IMAC)

    # Step 4: Click on 'Add to Cart' button in the displayed 'Product Display' page
    product_page.add_to_cart()

    # Validate ER-1: Success message with text - 'Success: You have added Product Name to your shopping cart!' should be displayed
    # Constructing the expected success message using constants to avoid hardcoding
    expected_success_msg = f"{PDP_ADD_TO_CART_SUCCESS_PREFIX} {TestData.PRODUCT_NAME_IMAC} {PDP_ADD_TO_CART_SUCCESS_SUFFIX}"
    expect(product_page.get_confirmation_message()).to_contain_text(expected_success_msg)

    # Step 5: Click on the 'shopping cart!' link in the displayed success message
    shopping_cart_page = product_page.click_shopping_cart_link()

    # Validate ER-2: Product should be successfully displayed in the 'Shopping Cart' page
    expect(shopping_cart_page.get_product_row_by_name(TestData.PRODUCT_NAME_IMAC)).to_be_visible()
