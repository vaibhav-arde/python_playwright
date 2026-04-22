"""
Test Case ID: #55
Test Case Description: Validate User can select number of products displayed in Search Results

1. Enter the search criteria in the 'Search' text box field which can result in multiple products
2. Click on the search button (Validate ER-1)
3. Select different values from the 'Show' dropdown (Validate ER-2)
"""

import pytest
import re
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.config import Config


@pytest.mark.ui
def test_products_limit(page):
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    search_term = Config.multiple_products_search_term
    limit_value = Config.product_limit

    # -------- Step 1: Search --------
    home_page.enter_product_name(search_term)
    home_page.click_search()

    # -------- ER-1 --------
    expect(search_results_page.get_search_results_page_header()).to_be_visible()

    total_products = search_results_page.get_product_count().count()
    assert total_products > 1

    # -------- ER-2 --------
    search_results_page.select_limit(limit_value)

    # Validate URL
    expect(page).to_have_url(re.compile(f"limit={limit_value}"))

    # Validate product count
    expected = min(int(limit_value), total_products)
    expect(search_results_page.get_product_count()).to_have_count(expected)
