"""
Test Case ID: #66
Description: Validate the Search functionality in all the supported environments

1. Enter any existing product name into the 'Search' text box field -
2. Click on the button having search icon (Validate ER-1)
"""

import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.config import Config


@pytest.mark.ui
@pytest.mark.cross_browser
def test_search_functionality_all_environments(page):
    home_page = HomePage(page)
    search_page = SearchResultsPage(page)

    home_page.open()

    home_page.enter_product_name(Config.product_name)
    home_page.click_search()

    expect(search_page.get_search_results_page_header()).to_be_visible()

    assert search_page.get_product_count().count() > 0

    expect(search_page.get_product_container(Config.product_name)).to_be_visible()
