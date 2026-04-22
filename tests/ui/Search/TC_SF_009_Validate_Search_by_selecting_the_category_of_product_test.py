"""
Test Case ID: #45
Description: Validate Search by selecting the category of product

1. Don't enter anything into the 'Search' text box field
2. Click on the button having search icon
3. Enter any Product Name into the 'Search Criteria' text box field -
4. Select the correct category of the given Product Name into 'Category' dropdown field -
5. Click on 'Search' button (Validate ER-1)
6. Select a wrong category in the 'Category' dropdown field - -
7. Click on 'Search' button (Validate ER-2)

"""

import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.config import Config


@pytest.mark.ui
@pytest.mark.critical
def test_search_using_search_criteria_field(page):
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    product_name = Config.product_name
    # Step 1: Don't enter anything into the 'Search' text box field
    # Step 2: Click on the button having search icon
    home_page.click_search()

    # Step 3: Enter any Product Name into the 'Search Criteria' text box field -
    search_results_page.enter_search_criteria(product_name)

    # Step 4: Select the correct category of the given Product Name into 'Category' dropdown field -
    search_results_page.select_category(Config.correct_category)

    # Step 5: Click on 'Search' button (Validate ER-1)
    search_results_page.click_search_criteria_button()

    # Wait for the results to load
    expect(search_results_page.get_search_results_page_header()).to_be_visible()
    # ER-1: Product should be visible
    expect(search_results_page.get_products_by_search_term(product_name).first).to_be_visible()

    # Step 6: Select a wrong category in the 'Category' dropdown field --
    search_results_page.enter_search_criteria(product_name)
    search_results_page.select_category(Config.wrong_category)

    # Step 7: Click on 'Search' button (Validate ER-2)
    search_results_page.click_search_criteria_button()

    # Wait for the results to load
    expect(search_results_page.get_search_results_page_header()).to_be_visible()

    # ER-2: Empty search message should be displayed
    expect(search_results_page.get_empty_search_message()).to_be_visible()
