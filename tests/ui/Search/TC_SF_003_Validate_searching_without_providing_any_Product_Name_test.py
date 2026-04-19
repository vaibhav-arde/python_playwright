"""
Test Case ID: #26
Description: Validate searching without providing any Product Name

Steps:

1. Don't enter anything into the 'Search' text box field
2. Click on the button having search icon (Validate ER-1)
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage


@pytest.mark.ui
def test_search_without_product_name(page):
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    # Step 1: Click search without entering any product name
    home_page.click_search()

    # Step 2: Validate search results
    # ER-1: Search results page should display the empty message
    expect(search_results_page.get_search_results_page_header()).to_contain_text("Search")
    expect(search_results_page.get_empty_search_message()).to_be_visible()
