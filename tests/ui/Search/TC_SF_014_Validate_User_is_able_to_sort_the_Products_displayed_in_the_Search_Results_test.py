"""
Test Case ID: #54
Test Case Description: Validate User is able to sort the Products displayed in the Search Results

1. Enter the search criteria in the 'Search' text box field which can result in mutliple products -
2. Click on the button having search icon (Validate ER-1)
3. Select several options from the 'Sort By' dropdown (Validate ER-2)

"""

import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.config import Config
from utils.constants import SortOptions


@pytest.mark.ui
def test_product_sort(page):
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    search_term = Config.multiple_products_search_term

    # Step 1: Search with multiple products
    home_page.enter_product_name(search_term)
    home_page.click_search()

    # Validate search results page
    expect(search_results_page.get_search_results_page_header()).to_be_visible()

    products = search_results_page.get_product_count()
    assert products.count() > 1

    # -------- SORT BY NAME (A → Z) --------
    search_results_page.select_sort_choice(SortOptions.NAME_ASC)
    search_results_page.verify_products_sorted(SortOptions.NAME_ASC)

    # -------- SORT BY PRICE (Low → High) --------
    search_results_page.select_sort_choice(SortOptions.PRICE_ASC)
    search_results_page.verify_products_sorted(SortOptions.PRICE_ASC)
