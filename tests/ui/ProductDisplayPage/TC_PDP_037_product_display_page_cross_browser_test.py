"""
TC_PDP_037
(TS_007) Product Display Page

Validate the Product Display Page functionality
in all supported environments

1. Open Application URL
2. Search existing product
3. Click search icon
4. Open product from search results
5. Validate PDP works correctly

Test Data:
Product Name: Apple Cinema 30"
"""

import pytest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.constants import TestData
from playwright.sync_api import expect, Page



@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.cross_browser
@pytest.mark.critical
def test_product_page_cross_browser(page: Page):
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    home_page.open_home_page()
    home_page.enter_product_name(TestData.PRODUCT_NAME_APPLE_CINEMA_30)
    home_page.click_search()

    product_page = search_results_page.select_product(TestData.PRODUCT_NAME_APPLE_CINEMA_30)

    # Explicit expectation in test script as per user requirement
    expect(product_page.lbl_product_name).to_be_visible()
    
    product_page.verify_product_page_functionality()
