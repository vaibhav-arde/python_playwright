import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData
from utils import messages


@pytest.mark.ui
@pytest.mark.regression
def test_validate_navigating_to_pdp_using_product_name_link_in_cart_button_toggle_box(authenticated_page):
    """
    Test Case ID: TC_PDP_030
    Validate navigating to the Product Display page by using the Product name link in the 'Cart' button toggle box
    """
    page = authenticated_page
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)


    # Step 2: Add product to cart
    home_page.open_home_page()
    home_page.enter_product_name(TestData.PRODUCT_NAME_IMAC)
    home_page.click_search()
    search_results_page.select_product(TestData.PRODUCT_NAME_IMAC)

    expected_name = product_page.get_product_name()
    product_page.add_to_cart()
    expect(product_page.get_confirmation_message()).to_be_visible()

    # Step 3: Click on Cart button to open toggle box
    product_page.click_items_to_navigate_to_cart()

    # Step 4: Click name link in the toggle box
    product_page.click_cart_name_link()

    # Validation: Navigate to PDP
    expect(product_page.get_page_heading()).to_be_visible(timeout=10000)
    actual_name = product_page.get_product_name()
    assert expected_name in actual_name, messages.PDP_PRODUCT_NAME_MISMATCH.format(
        expected=expected_name, actual=actual_name
    )
