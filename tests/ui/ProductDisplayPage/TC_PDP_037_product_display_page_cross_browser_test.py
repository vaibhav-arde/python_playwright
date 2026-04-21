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
Product Name: iMac
"""

import pytest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.config import Config


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.cross_browser
def test_product_page_cross_browser(page):
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    home_page.enter_product_name(Config.imac_product)
    home_page.click_search()

    product_page = search_results_page.select_product(Config.imac_product)

    product_page.verify_product_page_functionality()
