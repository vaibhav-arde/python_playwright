import pytest
from playwright.sync_api import Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData
from utils import messages


@pytest.mark.ui
@pytest.mark.regression
def test_validate_the_specifications(page: Page):
    """
    Test Case ID: TC_PDP_009
    Validate the specifications of the Product in the Product Display Page.
    """
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)

    # Step 1-3: Search and open the first product that exposes a Specification tab
    selected_product_name = TestData.EMPTY_VALUE
    for product_name in TestData.PRODUCTS_WITH_SPECIFICATION_TAB:
        home_page.enter_product_name(product_name)
        home_page.click_search()

        product_in_results = search_results_page.is_product_exist(product_name)
        assert product_in_results is not None, messages.SEARCH_RESULT_PRODUCT_NOT_FOUND.format(keyword=product_name)
        expected_product_name = search_results_page.get_text(product_in_results).strip()
        assert expected_product_name != TestData.EMPTY_VALUE, messages.SEARCH_RESULT_PRODUCT_NAME_EMPTY
        search_results_page.select_product(expected_product_name)

        if product_page.lnk_specification_tab.count() > 0 and product_page.lnk_specification_tab.is_visible():
            selected_product_name = expected_product_name
            break

    assert selected_product_name != TestData.EMPTY_VALUE, messages.PDP_SPECIFICATION_TAB_NOT_FOUND_FOR_PRODUCTS.format(
        products=TestData.COMMA_SPACE_SEPARATOR.join(TestData.PRODUCTS_WITH_SPECIFICATION_TAB)
    )

    # Step 4 (ER-1): Open Specification tab and validate specifications
    assert product_page.lnk_specification_tab.is_visible(), messages.PDP_SPECIFICATION_TAB_NOT_VISIBLE
    product_page.click_specification_tab()
    assert product_page.pnl_specification.is_visible(), messages.PDP_SPECIFICATION_PANEL_NOT_VISIBLE

    specification_text = product_page.get_specification_text()
    assert specification_text != TestData.EMPTY_VALUE, messages.PDP_SPECIFICATION_TEXT_EMPTY
