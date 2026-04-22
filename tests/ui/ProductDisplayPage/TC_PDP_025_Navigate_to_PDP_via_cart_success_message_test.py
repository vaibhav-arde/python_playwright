import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData
from utils import messages


@pytest.mark.ui
@pytest.mark.regression
def test_navigate_to_pdp_via_cart_success_message(page: Page):
    """
    Test Case ID: TC_PDP_025
    Validate navigating to the Product Display page by using the Product Name link in Success message on adding the Product to Cart

    Steps:
        1. Open the Application URL and Login
        2. Search for a product (iMac)
        3. Select the product from search results
        4. Click 'Add to Cart'
        5. Click on 'Product Name' link from the displayed success page

    Expected Result:
        User should be taken to the Product Display page of the Product.
    """
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)


    home_page.enter_product_name(TestData.PRODUCT_NAME_IMAC)
    home_page.click_search()

    product_in_results = search_results_page.is_product_exist(TestData.PRODUCT_NAME_IMAC)
    expected_product_name = search_results_page.get_text(product_in_results).strip()
    search_results_page.select_product(expected_product_name)

    # Step 4: Add to Cart
    product_page.add_to_cart()

    # Step 5: Click product name link in success message
    expect(product_page.get_confirmation_message()).to_be_visible()
    product_page.click_product_link_on_success_msg(expected_product_name)

    # Validate navigation to PDP
    expect(product_page.get_page_heading()).to_be_visible()
    assert product_page.get_product_name() == expected_product_name
