"""Test Case ID: #63

Validate we can use all the options of Search functionality using the Keyboard keys
"""

import re
import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.config import Config
from utils.constants import UIRoutes


@pytest.mark.ui
def test_search_functionality_using_keyboard_keys(page):
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    # Step 1: Navigate to Home Page
    home_page.open()

    # Step 2: Enter product name into the 'Search' text box field
    home_page.enter_product_name(Config.product_name)

    # Step 3: Press the 'Enter' key on the keyboard to search
    home_page.press_enter()

    # Step 4: Validate that we are on the Search page
    expect(search_results_page.get_search_results_page_header()).to_be_visible()
    expect(page).to_have_url(re.compile(UIRoutes.SEARCH_PAGE))

    # Step 5: Navigate to Search Criteria section using Keyboard (Tab)
    search_results_page.get_search_criteria_textbox().focus()

    # Step 6: Tab through options and select 'Search in product descriptions'
    home_page.press_tab(2)  # Category, Subcategories, Descriptions
    home_page.press_space()  # Toggle checkbox

    # Verify it is checked
    expect(search_results_page.get_search_in_descriptions_checkbox())

    # Step 7: Use Keyboard to navigate to Search button and press Enter
    home_page.press_tab()  # Move focus to Search button
    home_page.press_enter()

    # Step 8: Validate that the product is displayed in the search results
    expect(search_results_page.get_search_results_page_header()).to_contain_text(
        Config.product_name
    )
    expect(search_results_page.get_product_count()).not_to_have_count(0)
