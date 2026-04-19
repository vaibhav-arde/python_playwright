"""
Test Case ID: #19
Description: Validate searching using 'Search Criteria' field

1. Don't enter anything into the 'Search' text box field
2. Click on the button having search icon
3. Enter any existing product name into the 'Search Criteria' text box field
4. Click on 'Search' button (Validate ER-1)
"""

import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.config import Config


@pytest.mark.ui
def test_search_using_search_criteria_field(page):
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    # Step 1: Don't enter anything into the 'Search' text box field
    # Step 2: Click on the button having search icon
    home_page.click_search()

    # Step 3: Enter any existing product name into the 'Search Criteria' text box field
    search_results_page.enter_search_criteria(Config.product_name)

    # Step 4: Click on 'Search' button
    search_results_page.click_search_criteria_button()

    # Validate ER-1: Search results page should display the product
    expect(search_results_page.get_search_results_page_header()).to_be_visible()
