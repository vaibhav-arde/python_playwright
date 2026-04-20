import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData
from utils import messages


@pytest.mark.ui
@pytest.mark.regression
def test_validate_description_of_product(page: Page):
    """
    Test Case ID: TC_PDP_008
    Validate the description of product in Product Display Page.
    """
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)

    product_name = TestData.PRODUCT_NAME_IMAC

    # Step 1-3: Search and open product
    home_page.enter_product_name(product_name)
    home_page.click_search()

    product_in_results = search_results_page.is_product_exist(product_name)
    assert product_in_results is not None, messages.SEARCH_RESULT_PRODUCT_NOT_FOUND.format(keyword=product_name)
    expected_product_name = search_results_page.get_text(product_in_results).strip()
    assert expected_product_name != "", messages.SEARCH_RESULT_PRODUCT_NAME_EMPTY
    search_results_page.select_product(expected_product_name)

    # Step 4 (ER-1): Open Description tab and validate product description
    expect(product_page.lnk_description_tab.first).to_be_visible()
    product_page.click_description_tab()
    expect(product_page.pnl_description).to_be_visible()

    actual_description = product_page.get_description_text()
    assert actual_description != "", messages.PDP_DESCRIPTION_TEXT_EMPTY
