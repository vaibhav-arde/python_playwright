import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.constants import TestData


@pytest.mark.regression
@pytest.mark.ui
def test_atc_008_validate_ui_of_add_to_cart_functionality(page):
    """
    Test Case: TC_ATC_008 - Validate the UI of Add to Cart functionality

    Test Steps:
    1. Enter any existing Product name into the Search text box field - iMac
    2. Click on the button having search icon
    3. Click on the Product displayed in the Search results
    4. Validate the UI of 'Add to Cart' functionality in the Product Display Page:
       - Quantity Label/Field is visible
       - Default quantity is 1
       - 'Add to Cart' button is visible and enabled
       - Price is displayed
       - Availability status is displayed
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

    # Step 4: Validate the UI of 'Add to Cart' functionality in the Product Display Page

    # Validate Quantity Label/Field
    expect(product_page.txt_quantity).to_be_visible()

    # Validate Default quantity is 1
    # Using dynamic constant from TestData
    expect(product_page.txt_quantity).to_have_value(TestData.DEFAULT_QUANTITY)

    # Validate 'Add to Cart' button is visible and enabled
    expect(product_page.btn_add_to_cart).to_be_visible()
    expect(product_page.btn_add_to_cart).to_be_enabled()

    # Validate Price is displayed
    expect(product_page.lbl_product_price).to_be_visible()

    # Validate Availability status is displayed
    expect(product_page.lbl_product_availability).to_be_visible()
