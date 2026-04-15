"""
Test Case ID: #42
Description: Validate Search using the text from the product description

1. Don't enter anything into the 'Search' text box field
2. Click on the button having search icon
3. Enter any text from the Product Description into the 'Search Criteria' text box field -
4. Select 'Search in product descriptions' checkbox option
5. Click on 'Search' button (Validate ER-1)
"""

import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.config import ProductData


@pytest.mark.sanity
@pytest.mark.ui
def test_search_using_product_description(page):
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    # Grab the dictionary properties from the grouped datastructure
    desc_term = ProductData.IMAC["description_term"]
    product = ProductData.IMAC["expected_product"]

    # Step 1: Don't enter anything into the 'Search' text box field
    # Step 2: Click on the button having search icon
    home_page.click_search()

    # Step 3: Enter any text from the Product Description into the 'Search Criteria' text box field
    search_results_page.enter_search_criteria(desc_term)

    # Step 4: Select 'Search in product descriptions' checkbox option
    search_results_page.select_search_in_product_descriptions()

    # Step 5: Click on 'Search' button
    search_results_page.click_search_criteria_button()

    # Validate ER-1: Search results page should display the product
    expect(search_results_page.get_search_results_page_header()).to_be_visible()

    # Using locator.filter() which is faster and natively auto-waits
    filtered_product = search_results_page.get_products_by_search_term(product)
    expect(filtered_product).to_be_visible()
