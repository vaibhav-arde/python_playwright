import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.shopping_cart_page import ShoppingCartPage
from utils.constants import TestData
from utils.messages import PDP_ADD_TO_CART_SUCCESS_PREFIX, PDP_ADD_TO_CART_SUCCESS_SUFFIX


@pytest.mark.regression
@pytest.mark.ui
def test_atc_003_validate_adding_product_to_cart_from_search_results(page):
    """
    [TASK] TC_ATC_003 Validate adding the product to Cart from Search_Results_Page

    Test Steps:
    1. Enter any existing Product name into the Search text box field - iMac
    2. Click on the button having search icon
    3. Click on 'Add to Cart' option on the product that is displayed in the Search Results (Validate ER-1)
    4. Click on 'Cart' button which is in black color beside the search icon button on the top of the page
    5. Click on 'View Cart' option in the displayed box (Validate ER-2)
    """

    # Page Objects Initialization
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    shopping_cart_page = ShoppingCartPage(page)

    # Step 1: Enter any existing Product name into the Search text box field
    home_page.enter_product_name(TestData.PRODUCT_NAME_IMAC)

    # Step 2: Click on the button having search icon
    home_page.click_search()

    # Step 3: Click on 'Add to Cart' option on the product that is displayed in the Search Results
    search_results_page.click_add_to_cart(TestData.PRODUCT_NAME_IMAC)

    # Validate ER-1: Success message with text - 'Success: You have added Product Name to your shopping cart!' should be displayed
    expected_success_msg = f"{PDP_ADD_TO_CART_SUCCESS_PREFIX} {TestData.PRODUCT_NAME_IMAC} {PDP_ADD_TO_CART_SUCCESS_SUFFIX}"
    expect(search_results_page.get_confirmation_message()).to_contain_text(expected_success_msg)

    # Step 4: Click on 'Cart' button which is in black color beside the search icon button on the top of the page
    home_page.click_cart_total_button()

    # Step 5: Click on 'View Cart' option in the displayed box
    home_page.click_view_cart()

    # Validate ER-2: Product should be successfully displayed in the 'Shopping Cart' page
    expect(shopping_cart_page.get_product_row_by_name(TestData.PRODUCT_NAME_IMAC)).to_be_visible()
