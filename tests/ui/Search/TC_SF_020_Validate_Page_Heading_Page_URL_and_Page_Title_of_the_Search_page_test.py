"""
Test Case ID: #64
Description: Validate Page Heading, Page URL and Page Title of the Search page

1. Enter any existing product name into the 'Search' text box field
2. Click on the button having search icon
3. Check the Page Heading, Page URL and Page Title of the 'Search' page

"""

import pytest
import re
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.config import Config
from utils.constants import UIRoutes


@pytest.mark.ui
def test_page_heading_page_url_and_page_title_of_the_search_page(page):
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    # Step 1: Enter any existing product name into the 'Search' text box field
    home_page.enter_product_name(Config.product_name)

    # Step 2: Click on the button having search icon
    home_page.click_search()

    # Step 3: Validate the Page Heading, Page URL and Page Title of the Search page
    expect(search_results_page.get_search_results_page_header()).to_be_visible()
    expect(page).to_have_url(re.compile(UIRoutes.SEARCH_PAGE))
    expect(page).to_have_title(f"Search - {Config.product_name}")
