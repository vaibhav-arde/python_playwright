"""
Test Case ID: #19
Description: Validate searching with an existing product name

1. Enter any existing product name into the 'Search' text box field
2. Click on the button having search icon (Validate ER-1)

"""

import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.config import Config


@pytest.mark.sanity
@pytest.mark.ui
def test_search_with_existing_product_name(page):
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    # Step 1: Enter existing product name
    home_page.enter_product_name(Config.product_name)
    home_page.click_search()

    # Step 2: Validate search results
    # ER-1: Search results page should display the product
    expect(search_results_page.get_search_results_page_header()).to_contain_text(
        Config.product_name
    )
    expect(search_results_page.is_product_exist(Config.product_name)).to_be_visible()
