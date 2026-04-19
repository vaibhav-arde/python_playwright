"""
Test Case ID: #57
Description: Validate Breadcrumb of the Search page

1. Enter any existing product name into the 'Search' text box field
2. Click on the button having search icon
3. Validate the breadcrumb of the Search page

"""

import pytest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.config import Config


@pytest.mark.ui
def test_breadcrumb_of_the_search_page(page):
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    # Step 1: Enter any existing product name into the 'Search' text box field
    home_page.enter_product_name(Config.product_name)

    # Step 2: Click on the button having search icon
    home_page.click_search()

    search_results_page.validate_breadcrumb()
