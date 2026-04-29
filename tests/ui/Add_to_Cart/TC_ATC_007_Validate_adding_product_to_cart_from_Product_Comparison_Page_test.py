import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_comparison_page import ProductComparisonPage
from pages.shopping_cart_page import ShoppingCartPage
from utils import messages
from utils.constants import TestData, UILabels


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.add_to_cart
def test_atc_007_validate_adding_product_to_cart_from_product_comparison_page(page: Page):
    """
    TC_ATC_007: Validate adding the product to Cart from_Product_Comparison_Page

    Pre-requisites:
    1. Open the Application URL
    2. A product is added to Product Comparison page - iMac

    Test Steps:
    1. Click on 'Add to Cart' button on the product that is displayed in the 'Product Comparison' page (Validate ER-1)
    2. Click on the 'shopping cart!' link in the displayed success message (Validate ER-2)

    Expected Result (ER):
    1. Success message with text - 'Success: You have added Product Name to your shopping cart!' should be displayed
    2. Product should be successfully displayed in the 'Shopping Cart' page
    """

    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    comparison_page = ProductComparisonPage(page)
    shopping_cart_page = ShoppingCartPage(page)

    # Pre-requisite 1: Open the Application URL
    home_page.open_home_page()

    # Pre-requisite 2: A product is added to Product Comparison page
    # Search for the product
    home_page.enter_product_name(TestData.PRODUCT_NAME_IMAC)
    home_page.click_search()

    # Add to comparison
    search_results_page.click_compare_this_product(TestData.PRODUCT_NAME_IMAC)

    # Navigate to Comparison Page via success message link
    search_results_page.click_comparison_link_in_success_msg()
    expect(comparison_page.lbl_heading).to_be_visible()

    # Step 1: Click on 'Add to Cart' button on the product in 'Product Comparison' page
    comparison_page.click_add_to_cart(TestData.PRODUCT_NAME_IMAC)

    # Validate ER-1: Success message should be displayed
    expect(comparison_page.get_confirmation_message()).to_be_visible()
    expect(comparison_page.get_confirmation_message()).to_contain_text(TestData.PRODUCT_NAME_IMAC)
    expect(comparison_page.get_confirmation_message()).to_contain_text(
        messages.PDP_ADD_TO_CART_SUCCESS_PREFIX
    )
    expect(comparison_page.get_confirmation_message()).to_contain_text(
        messages.PDP_ADD_TO_CART_SUCCESS_SUFFIX
    )

    # Step 2: Click on the 'shopping cart!' link in the success message
    comparison_page.click_shopping_cart_link_in_success_msg()

    # Validate ER-2: Product should be successfully displayed in the 'Shopping Cart' page
    expect(shopping_cart_page.lbl_cart_page_header).to_be_visible()
    expect(shopping_cart_page.lbl_cart_page_header).to_contain_text(UILabels.CART_PAGE_HEADING)

    # Verify the specific product is present in the cart
    is_present = shopping_cart_page.is_product_in_cart(TestData.PRODUCT_NAME_IMAC)
    assert is_present, messages.PRODUCT_NOT_IN_CART.format(product=TestData.PRODUCT_NAME_IMAC)
