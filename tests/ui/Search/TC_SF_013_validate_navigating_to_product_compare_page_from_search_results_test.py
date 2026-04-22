"""
Test Case ID: #52
Description: Validate navigating to product compare page from search results

1. Enter any existing product name into the 'Search' text box field -
2. Click on the button having search icon
3. Click on the 'Product Compare' link (Validate ER-1)

"""

import pytest
import re
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.config import Config
from utils.constants import UIRoutes


@pytest.mark.ui
def test_product_compare_navigation(page):
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    product_name = Config.product_name

    # Step 1: Enter existing product name
    home_page.enter_product_name(product_name)

    # Step 2: Click search icon
    home_page.click_search()

    # Step 3: Add product to compare
    search_results_page.click_compare(product_name)

    # Step 4: Click Product Compare link (actual navigation)
    search_results_page.click_product_compare_link()

    # ER-1: Should navigate to product compare page
    expect(page).to_have_url(re.compile(UIRoutes.PRODUCT_COMPARE_PAGE))
