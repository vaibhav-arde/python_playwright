import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from pages.shopping_cart_page import ShoppingCartPage
from pages.registration_page import RegistrationPage
from utils.constants import TestData
from utils import messages
from utils.random_test_data import RandomTestData


@pytest.mark.ui
@pytest.mark.regression
def test_validate_navigating_to_pdp_using_product_name_link_in_shopping_cart_page(page: Page):
    """
    Test Case ID: TC_PDP_027
    Validate navigating to the Product Display page by using the Product name link in the 'Shopping Cart' page
    """
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)
    shopping_cart_page = ShoppingCartPage(page)
    registration_page = RegistrationPage(page)


    # Step 1: Register a new account to ensure active session and clean context
    home_page.open_home_page()
    home_page.click_my_account()
    home_page.click_register()

    unique_user = RandomTestData.get_user()
    registration_page.complete_registration(unique_user)
    expect(registration_page.get_confirmation_msg()).to_be_visible()

    # Step 2: Add product to cart
    home_page.open_home_page()
    home_page.enter_product_name(TestData.PRODUCT_NAME_IMAC)
    home_page.click_search()
    search_results_page.select_product(TestData.PRODUCT_NAME_IMAC)

    expected_name = product_page.get_product_name()
    product_page.add_to_cart()
    expect(product_page.get_any_alert_message()).to_be_visible()

    # Step 3: Go to Shopping Cart page
    product_page.click_shopping_cart_link()
    expect(shopping_cart_page.get_page_heading()).to_be_visible()

    # Step 4: Click name link in shopping cart table
    shopping_cart_page.click_product_name(expected_name)

    # Validation: Navigate to PDP
    expect(product_page.get_page_heading()).to_be_visible()
    actual_name = product_page.get_product_name()
    assert expected_name in actual_name, messages.PDP_PRODUCT_NAME_MISMATCH.format(
        expected=expected_name, actual=actual_name
    )
