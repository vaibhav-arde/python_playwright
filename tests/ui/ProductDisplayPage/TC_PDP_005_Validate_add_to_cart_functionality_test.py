import pytest
from playwright.sync_api import expect, Page, TimeoutError as PlaywrightTimeoutError
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData, UITimeouts
from utils import messages


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.sanity
@pytest.mark.critical
def test_validate_add_to_cart_functionality(page: Page):
    """
    Test Case ID: TC_PDP_005
    Validate the 'Add to Cart' functionality including quantity selection and success notification.
    """
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)

    # Step 1-3: Search and Navigate to Product
    home_page.enter_product_name(TestData.PRODUCT_NAME_IMAC)
    home_page.click_search()
    search_results_page.select_product(TestData.PRODUCT_NAME_IMAC)

    # Step 4: Set Quantity and Add to Cart
    target_quantity = TestData.CART_TARGET_QUANTITY
    product_page.set_quantity(target_quantity)
    product_page.add_to_cart()

    # Step 5: Validate Success Message
    # ER: Success message should be displayed for adding the product to cart

    success_msg = product_page.get_confirmation_message()
    try:
        expect(success_msg).to_be_visible(timeout=UITimeouts.CART_ALERT_WAIT_MS)
    except PlaywrightTimeoutError:
        # Retry once for occasional transient miss-click/network lag on demo site.
        product_page.add_to_cart()
        expect(success_msg).to_be_visible(timeout=UITimeouts.CART_ALERT_WAIT_MS)

    # ER: Success message should contain product name and success text
    expect(success_msg).to_contain_text(TestData.PRODUCT_NAME_IMAC)
    expect(success_msg).to_contain_text(messages.PDP_ADD_TO_CART_SUCCESS_PREFIX)
