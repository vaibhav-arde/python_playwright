"""
Test Case: Product Search Functionality

===========================================
Test Steps
===========================================
1. Enter a product name in the search box.
2. Click the Search button.
3. Verify the Search Results page is displayed.
4. Verify the searched product appears in results.
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.config import Config


@pytest.mark.sanity
@pytest.mark.regression
def test_product_search(page):
    product_name = Config.product_name

    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    home_page.enter_product_name(product_name)
    home_page.click_search()

    expect(search_results_page.get_search_results_page_header()).to_be_visible(
        timeout=5000
    )
    expect(search_results_page.is_product_exist(product_name)).to_be_visible(
        timeout=5000
    )
