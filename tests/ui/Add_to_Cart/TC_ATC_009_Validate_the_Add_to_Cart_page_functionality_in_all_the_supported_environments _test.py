import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.constants import TestData


@pytest.mark.regression
@pytest.mark.cross_browser
@pytest.mark.add_to_cart
def test_atc_009_validate_add_to_cart_functionality_in_all_environments(page):
    """
    Test Case: TC_ATC_009 - Validate the 'Add to Cart' page functionality in all the supported environments

    Pre-requisites:
    1. Open the Application URL in any supported browser

    Test Steps:
    1. Check the 'Add to Cart' functionality in all the supported environments (Validate ER-1)

    Expected Result:
    1. 'Add to Cart' functionality should work correctly in all the supported environments
    """

    # Page Objects Initialization
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    # Step 1: Search for the product (iMac)
    # Using Playwright advanced locator via POM method
    home_page.enter_product_name(TestData.PRODUCT_NAME_IMAC)
    home_page.click_search()

    # Step 2: Select the product from search results to navigate to Product Display Page (PDP)
    # This validates the transition and availability on the PDP
    product_page = search_results_page.select_product(TestData.PRODUCT_NAME_IMAC)

    # Step 3: Add the product to cart from PDP
    # Validate the core 'Add to Cart' functionality
    product_page.set_quantity(TestData.DEFAULT_QUANTITY)
    product_page.add_to_cart()

    # Step 4: Validate the success message
    expect(product_page.get_confirmation_message()).to_be_visible()
    expect(product_page.get_confirmation_message()).to_contain_text(TestData.PRODUCT_NAME_IMAC)

    # Step 5: Navigate to Shopping Cart and verify product presence
    # This ensures the product was actually added to the backend/session cart
    shopping_cart_page = product_page.click_shopping_cart_link()

    # Verify page heading and product in cart
    expect(shopping_cart_page.get_page_heading()).to_be_visible()

    # Dynamic assertion: Use expect on the locator returned by POM to handle retries
    expect(shopping_cart_page.get_product_row_by_name(TestData.PRODUCT_NAME_IMAC)).to_be_visible()
