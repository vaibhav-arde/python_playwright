"""
Test Case ID: #65
Description: Validate the UI of Search functionality and Search page options

1. Enter any existing product name into the 'Search' text box field
2. Click on the button having search icon (Validate ER-1)

Acceptance Criteria:

1. Proper UI rendering to the UI checklist should be displayed for the complete Search functionality

"""

import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.config import Config


@pytest.mark.ui
def test_search_functionality_ui(page):
    home_page = HomePage(page)
    search_page = SearchResultsPage(page)

    # Step 1: Enter product name
    home_page.enter_product_name(Config.product_name)

    # Step 2: Click search icon
    home_page.click_search()

    # Page Header
    expect(search_page.get_search_results_page_header()).to_be_visible()

    # Search Criteria Section
    expect(search_page.get_search_criteria_textbox()).to_be_visible()
    expect(search_page.get_category_dropdown()).to_be_visible()
    expect(search_page.get_search_button()).to_be_visible()
    expect(search_page.get_search_in_descriptions_checkbox()).to_be_visible()
    expect(search_page.get_search_in_subcategories_checkbox()).to_be_visible()
    expect(search_page.get_search_criteria_textbox()).to_have_value(Config.product_name)

    # Breadcrumb Validation
    search_page.validate_breadcrumb()

    # View Options
    expect(search_page.get_list_view_button()).to_be_visible()
    expect(search_page.get_grid_view_button()).to_be_visible()

    # Sort & Limit Dropdowns
    expect(search_page.get_sort_dropdown()).to_be_visible()
    expect(search_page.get_limit_dropdown()).to_be_visible()

    # Ensure at least 1 product is present
    expect(search_page.get_product_count().first).to_be_visible()

    # Validate specific product container
    expect(search_page.get_product_container(Config.product_name)).to_be_visible()
