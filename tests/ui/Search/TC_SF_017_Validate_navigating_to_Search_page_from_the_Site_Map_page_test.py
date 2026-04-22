"""
Test Case ID: #60
Test Case Description: Validate navigating to Search page from the Site Map page

1. Click on 'Site Map' link in the footer options
2 .Click on the 'Search' link from the 'Site Map' page (Validate ER-1)

"""

import pytest
import re
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.site_map_page import SiteMapPage
from utils.constants import UIRoutes


@pytest.mark.ui
def test_navigate_to_search_from_site_map(page):
    home_page = HomePage(page)
    site_map_page = SiteMapPage(page)
    search_results_page = SearchResultsPage(page)

    # 1. Navigate to Home Page
    home_page.open(UIRoutes.HOME)

    # 2. Click on 'Site Map' link in the footer
    home_page.click_site_map()

    # 3. Click on the 'Search' link from the 'Site Map' page
    site_map_page.click_search_link()

    # 4. Validate that we are on the Search page
    expect(search_results_page.get_search_results_page_header()).to_be_visible()
    expect(page).to_have_url(re.compile(UIRoutes.SEARCH_PAGE))
