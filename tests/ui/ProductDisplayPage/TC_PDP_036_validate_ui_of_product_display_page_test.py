"""
TC_PDP_036
(TS_007) Product Display Page

1. Open Application URL
2. Search for existing product
3. Click search icon
4. Open product from search results
5. Validate Product Display Page UI

Test Data:
Product Name: iMac"""

import pytest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.config import Config


@pytest.mark.ui
@pytest.mark.regression
def test_pdp_ui_validation(page, base_url):
    page.goto(base_url)

    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    home_page.enter_product_name(Config.imac_product)
    home_page.click_search()

    product_page = search_results_page.select_product(Config.imac_product)

    product_page.verify_product_page_ui()
