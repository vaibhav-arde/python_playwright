import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData
from utils import messages


@pytest.mark.ui
@pytest.mark.regression
def test_validate_related_products_navigation(page: Page):
    """
    Test Case ID: TC_PDP_022
    Validate 'Related Products' section in Product Display page
    """
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)

    # Use a product known to have related products in the demo data
    product_name = TestData.PRODUCT_NAME_APPLE_CINEMA_30

    home_page.enter_product_name(product_name)
    home_page.click_search()

    product_in_results = search_results_page.is_product_exist(product_name)
    assert product_in_results is not None, messages.SEARCH_RESULT_PRODUCT_NOT_FOUND.format(
        keyword=product_name
    )

    expected_product_name = search_results_page.get_text(product_in_results).strip()
    search_results_page.select_product(expected_product_name)

    # Step 4: Validate Related Products
    # Scroll to ensure it's loaded if lazy
    product_page.pnl_related_products.scroll_into_view_if_needed()
    expect(product_page.pnl_related_products).to_be_visible(), messages.RELATED_PRODUCT_NOT_FOUND

    count = product_page.get_related_products_count()
    assert count > 0, messages.RELATED_PRODUCT_NOT_FOUND

    # Click the first related product
    # Capture name before clicking to verify navigation
    related_product_element = product_page.lnk_related_product.first
    related_product_name = related_product_element.inner_text().strip()

    product_page.click_related_product(0)

    # Verify navigation to the new PDP by checking heading
    expect(product_page.lbl_product_name).to_be_visible(timeout=10000)
    actual_name = product_page.get_product_name()
    assert (
        related_product_name in actual_name
    ), f"Expected PDP for {related_product_name}, but got {actual_name}"
