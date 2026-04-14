"""
Test Case ID: #21
Description: Validate searching with a non-existing product name

1. Enter any non-existing product name into the 'Search' text box field
2. Click on the button having search icon (Validate ER-1)

"""

import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.config import Config


@pytest.mark.sanity
@pytest.mark.ui
def test_search_with_non_existing_product_name(page):
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    # Step 1: Enter non-existing product name
    home_page.enter_product_name(Config.invalid_product_name)
    home_page.click_search()

    # Step 2: Validate search results
    # ER-1: Search results page should display the empty message
    expect(search_results_page.get_search_results_page_header()).to_contain_text(
        Config.invalid_product_name
    )
    expect(search_results_page.get_empty_search_message()).to_be_visible()
