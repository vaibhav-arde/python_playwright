"""
Test Case ID: #45
Description: Validate Search by selecting the category of product

1. Don't enter anything into the 'Search' text box field
2. Click on the button having search icon
3. Enter any Product Name into the 'Search Criteria' text box field -
4. Select the Parent category of the given Product Name into 'Category' dropdown field -
5. Click on 'Search' button (Validate ER-1)
6. Select 'Search in subcategories' checkbox field
Click on 'Search' button (Validate ER-2)

"""

import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.config import Config
from utils.assertions import assert_products_match_search


@pytest.mark.sanity
@pytest.mark.ui
def test_search_by_selecting_to_search_in_subcategories(page):
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    # Step 1: Don't enter anything into the 'Search' text box field
    # Step 2: Click on the button having search icon
    home_page.click_search()

    # Step 3: Enter any Product Name into the 'Search Criteria' text box field
    search_results_page.enter_search_criteria(Config.product_name)

    # Step 4: Select the Parent category of the given Product Name into 'Category' dropdown field
    search_results_page.select_category(Config.parent_category)

    # Step 5: Click on 'Search' button (Validate ER-1)
    search_results_page.click_search_criteria_button()

    # Validate ER-1: Search results page should display the product
    expect(search_results_page.get_empty_search_message()).to_be_visible()

    # Step 6: Select 'Search in subcategories' checkbox field
    search_results_page.select_search_in_subcategories()

    # Step 7: Click on 'Search' button (Validate ER-2)
    search_results_page.click_search_criteria_button()

    # Validate ER-2: Search results page should display the product
    expect(search_results_page.get_search_results_page_header()).to_be_visible()

    # Validate that products match the search criteria
    products = search_results_page.get_product_count()
    assert_products_match_search(products, Config.product_name)
