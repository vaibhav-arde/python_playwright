import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage
from pages.shopping_cart_page import ShoppingCartPage
from utils import messages
from utils.constants import TestData, UILabels


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.add_to_cart
def test_atc_006_validate_adding_product_to_cart_from_featured_section(page: Page):
    """
    TC_ATC_006: Validate adding the product to Cart from the Products displayed in the 'Featured' section of Home page

    Pre-requisites:
    1. Open the Application URL

    Test Steps:
    1. Click on 'Add to Cart' button on the product that is displayed in the 'Featured' section of the Home page (Validate ER-1)
    2. Click on the 'shopping cart!' link in the displayed success message (Validate ER-2)

    Expected Result (ER):
    1. Success message with text - 'Success: You have added Product Name to your shopping cart!' should be displayed
    2. Product should be successfully displayed in the 'Shopping Cart' page
    """

    home_page = HomePage(page)
    shopping_cart_page = ShoppingCartPage(page)

    # Pre-requisite: Open the Application URL
    # (Note: navigate_to_base_url fixture in fixtures/browser.py handles this if autouse=True)
    home_page.open_home_page()

    # Step 1: Click on 'Add to Cart' button on the product displayed in 'Featured' section
    # Using a constant for the product name to avoid hardcoding
    home_page.click_add_to_cart_of_featured_product(TestData.PRODUCT_NAME_MACBOOK)

    # Validate ER-1: Success message should be displayed with expected text
    expect(home_page.get_confirmation_message()).to_be_visible()
    expect(home_page.get_confirmation_message()).to_contain_text(TestData.PRODUCT_NAME_MACBOOK)
    expect(home_page.get_confirmation_message()).to_contain_text(
        messages.PDP_ADD_TO_CART_SUCCESS_PREFIX
    )
    expect(home_page.get_confirmation_message()).to_contain_text(
        messages.PDP_ADD_TO_CART_SUCCESS_SUFFIX
    )

    # Step 2: Click on the 'shopping cart!' link in the displayed success message
    home_page.click_shopping_cart_link_in_success_msg()

    # Validate ER-2: Product should be successfully displayed in the 'Shopping Cart' page
    expect(shopping_cart_page.lbl_cart_page_header).to_be_visible()
    expect(shopping_cart_page.lbl_cart_page_header).to_contain_text(UILabels.CART_PAGE_HEADING)

    # Verify the specific product is present in the cart
    is_present = shopping_cart_page.is_product_in_cart(TestData.PRODUCT_NAME_MACBOOK)
    assert is_present, messages.PRODUCT_NOT_IN_CART.format(product=TestData.PRODUCT_NAME_MACBOOK)
