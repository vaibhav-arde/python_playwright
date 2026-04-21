import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from pages.shopping_cart_page import ShoppingCartPage
from utils.constants import TestData, UIRoutes
from utils import messages


@pytest.mark.ui
@pytest.mark.regression
def test_validate_product_having_minimum_quantity_set(page: Page):
    """
    Test Case ID: TC_PDP_007
    Validate product behavior when minimum quantity is configured.
    """
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)

    product_name = TestData.PRODUCT_NAME_APPLE_CINEMA_30

    # Step 1-3: Search and open the product
    home_page.enter_product_name(product_name)
    home_page.click_search()

    product_in_results = search_results_page.is_product_exist(product_name)
    assert product_in_results is not None, messages.SEARCH_RESULT_PRODUCT_NOT_FOUND.format(
        keyword=product_name
    )
    expected_product_name = product_in_results.text_content().strip()
    assert expected_product_name != "", messages.SEARCH_RESULT_PRODUCT_NAME_EMPTY
    search_results_page.select_product(expected_product_name)

    # Step 4 (ER-1): Default quantity and minimum quantity info should be shown
    expect(product_page.txt_quantity).to_be_visible()
    actual_default_qty = product_page.get_default_quantity_value()
    assert (
        actual_default_qty == TestData.MINIMUM_PRODUCT_QUANTITY
    ), messages.PDP_DEFAULT_QTY_MISMATCH.format(
        expected=TestData.MINIMUM_PRODUCT_QUANTITY, actual=actual_default_qty
    )

    minimum_qty_info = product_page.get_minimum_quantity_info_text()
    assert minimum_qty_info != "", messages.PDP_MIN_QTY_INFO_EMPTY
    assert (
        TestData.MINIMUM_PRODUCT_QUANTITY in minimum_qty_info
    ), messages.PDP_MIN_QTY_INFO_MISSING_VALUE.format(
        expected=TestData.MINIMUM_PRODUCT_QUANTITY, actual=minimum_qty_info
    )

    # Step 5 (ER-2): Reduce below minimum, add to cart and validate warning + cart behavior
    product_page.set_quantity(TestData.BELOW_MINIMUM_PRODUCT_QUANTITY)
    product_page.add_to_cart()
    product_page.wait_for_cart_feedback()

    feedback_text = " ".join(product_page.any_alert_msg.all_text_contents()).strip()
    assert feedback_text != "", messages.PDP_MIN_QTY_WARNING_NOT_VISIBLE
    assert (
        TestData.MINIMUM_PRODUCT_QUANTITY in feedback_text
    ), messages.PDP_MIN_QTY_WARNING_MISSING_QTY.format(
        qty=TestData.MINIMUM_PRODUCT_QUANTITY, actual=feedback_text
    )
    assert (
        messages.PDP_MIN_QTY_KEYWORD in feedback_text.lower()
    ), messages.PDP_MIN_QTY_WARNING_MISSING_KEYWORD.format(actual=feedback_text)

    shopping_cart_page = ShoppingCartPage(page)
    app_base_url = page.url.split(UIRoutes.INDEX_ENTRY)[0]
    shopping_cart_page.open(f"{app_base_url}{UIRoutes.CART.lstrip('/')}")
    expect(page.locator("#content")).to_contain_text(messages.CART_EMPTY_TEXT)

    # Step 6 (ER-3): Increase quantity beyond minimum and add to cart again
    home_page.enter_product_name(product_name)
    home_page.click_search()
    search_results_page.select_product(product_name)
    product_page.set_quantity(TestData.ABOVE_MINIMUM_PRODUCT_QUANTITY)
    product_page.add_to_cart()
    product_page.wait_for_cart_feedback()

    final_feedback_text = " ".join(product_page.any_alert_msg.all_text_contents()).strip()
    assert final_feedback_text != "", messages.PDP_ADD_TO_CART_FEEDBACK_EMPTY
    assert (
        messages.SUCCESS_ALERT_KEYWORD.lower() in final_feedback_text.lower()
        or messages.PDP_MIN_QTY_KEYWORD in final_feedback_text.lower()
    ), messages.PDP_ADD_TO_CART_FEEDBACK_UNEXPECTED.format(actual=final_feedback_text)
