import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from pages.checkout_page import CheckoutPage
from pages.shopping_cart_page import ShoppingCartPage
from utils.constants import TestData, UIRoutes
from utils.config import Config
from utils import messages


@pytest.mark.ui
@pytest.mark.regression
def test_validate_navigating_to_pdp_using_product_name_link_in_checkout_page(page: Page):
    """
    Test Case ID: TC_PDP_028
    Validate navigating to the Product Display page by using the Product Name link in the 'Confirm Order' section of the 'Checkout' page.
    """
    home_page = HomePage(page)
    login_page = LoginPage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)
    shopping_cart_page = ShoppingCartPage(page)
    checkout_page = CheckoutPage(page)
    
    product_name = TestData.PRODUCT_NAME_HTC

    # Step 1: Open the Application URL and Login
    home_page.click_my_account()
    home_page.click_login()
    login_page.login(Config.email, Config.password)

    # Clear Cart to handle previous test data
    page.goto(UIRoutes.CART)
    shopping_cart_page.clear_cart()
    page.goto("/") # Go back to home for next steps
    page.wait_for_load_state("networkidle")

    # Step 2-3: Enter Product Name and Click Search icon
    home_page.enter_product_name(product_name)
    home_page.click_search()

    # Step 4: Click on the Product displayed in the Search results
    search_results_page.select_product(product_name)

    # Step 4 continued: Click on 'Add to Cart' button
    product_page.add_to_cart()
    expect(product_page.get_confirmation_message()).to_be_visible()

    # Step 5: Click on 'Checkout' button in the displayed 'Shopping Cart' page
    # Instead of shopping cart page, I'll go directly to checkout if possible, 
    # but the instructions say "in the displayed Shopping Cart page".
    shopping_cart_page = product_page.click_shopping_cart_link()
    checkout_page = shopping_cart_page.click_on_checkout()

    # Step 6: Click on 'Continue' buttons and select any mandatory checkboxes until you reach the 'Confirm Order' section
    # Stage 1: Billing Details
    checkout_page.click_continue_after_billing_address()
    
    # Stage 2: Delivery Details
    checkout_page.click_continue_after_delivery_address()
    
    # Stage 3: Delivery Method
    checkout_page.click_continue_after_delivery_method()
    
    # Stage 4: Payment Method
    checkout_page.select_terms_and_conditions()
    checkout_page.click_continue_after_payment_method()

    # Step 7 (ER-1): Click on 'Product Name' link in the 'Confirm Order' section
    # Wait, if the method wasn't added, I'll use a direct locator here for now to ensure test works, 
    # but I'll try to add it again after.
    # Actually, I'll use the method I intended to add.
    new_product_page = checkout_page.click_product_name_confirm()

    # Validation: User should be taken to the Product Display page of the Product
    expect(new_product_page.lbl_product_name).to_be_visible()
    actual_product_name = new_product_page.get_product_name()
    assert actual_product_name == product_name, messages.PDP_PRODUCT_NAME_MISMATCH.format(
        expected=product_name, actual=actual_product_name
    )
