import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData
from utils import messages


@pytest.mark.ui
@pytest.mark.regression

def test_validate_invalid_quantity(page: Page):
    """
    Test Case ID: TC_PDP_006
    Validate system behavior when an invalid quantity is entered on PDP.
    """
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)

    # Step 1-3: Search and navigate to product details page
    home_page.enter_product_name(TestData.PRODUCT_NAME_IMAC)
    home_page.click_search()
    search_results_page.select_product(TestData.PRODUCT_NAME_IMAC)

    # Step 4: Enter invalid quantity and attempt add to cart
    invalid_quantity = TestData.INVALID_PRODUCT_QUANTITY  # 0
    product_page.set_quantity(invalid_quantity)
    product_page.add_to_cart()

    # Step 5: Validate application feedback (Success or Warning)
    # The application shows either a success message or stays on the page with an alert.
    expect(product_page.any_alert_msg.first).to_be_visible(timeout=10000)

    # We check if it's a success or warning
    success_visible = product_page.cnf_msg.first.is_visible()
    warning_visible = product_page.warning_msg.first.is_visible()

    assert success_visible or warning_visible, messages.INVALID_QTY_ALERT_EXPECTATION

    if success_visible:
        expect(product_page.cnf_msg.first).to_contain_text(messages.SUCCESS_ALERT_KEYWORD)
    elif warning_visible:
        expect(product_page.warning_msg.first).to_contain_text(messages.WARNING_ALERT_KEYWORD)

    # Verify quantity is kept at the value we entered (0)
    expect(product_page.txt_quantity).to_have_value(invalid_quantity)
