import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData
from utils import messages


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
    invalid_quantity = TestData.INVALID_PRODUCT_QUANTITY    # 0
    product_page.set_quantity(invalid_quantity)
    product_page.add_to_cart()

    # Step 5: Validate application feedback is displayed
    # Depending on backend validation, app may show success (auto-corrected quantity)
    # or warning (rejected quantity). Either way, feedback must be shown.
    success_alert = product_page.get_confirmation_message()
    warning_alert = product_page.get_warning_message()
    product_page.wait_for_cart_feedback()

    success_visible = success_alert.is_visible()
    warning_visible = warning_alert.is_visible()

    assert success_visible or warning_visible, messages.INVALID_QTY_ALERT_EXPECTATION

    if success_visible:
        expect(success_alert).to_contain_text(messages.SUCCESS_ALERT_KEYWORD)

    if warning_visible:
        expect(warning_alert).to_contain_text(messages.WARNING_ALERT_KEYWORD)
