"""
Test Case ID: #37
Description: Validate searching by providing a search criteria which results in multiple products

Enter the search criteria in the 'Search' text box field which can result in multiple products -
Click on the button having search icon (Validate ER-1)

"""

import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.config import Config
from utils.assertions import assert_products_match_search


@pytest.mark.ui
def test_search_with_multiple_products(page):
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    # Step 1: Enter search criteria which results in multiple products
    home_page.enter_product_name(Config.multiple_products_search_term)
    home_page.click_search()

    # Step 2: Validate search results
    # ER-1: Search results page should display multiple products
    expect(search_results_page.get_search_results_page_header()).to_be_visible()

    # Validate that products match the search criteria
    products = search_results_page.get_product_count()
    assert_products_match_search(products, Config.multiple_products_search_term)
