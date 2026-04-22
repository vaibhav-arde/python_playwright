import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from pages.registration_page import RegistrationPage
from utils.constants import TestData
from utils import messages
from utils.random_test_data import RandomTestData

@pytest.mark.ui
@pytest.mark.regression
def test_validate_navigating_to_pdp_using_product_name_link_in_cart_button_toggle_box(page: Page):
    """
    Test Case ID: TC_PDP_030
    Validate navigating to the Product Display page by using the Product name link in the 'Cart button toggle box'.
    """
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)
    registration_page = RegistrationPage(page)

    product_name = TestData.PRODUCT_NAME_IMAC

    # Step 1: Register a new account to ensure active session and clean context
    home_page.open_home_page()
    home_page.click_my_account()
    home_page.click_register()
    
    unique_user = RandomTestData.get_user()
    registration_page.complete_registration(unique_user)
    expect(registration_page.get_confirmation_msg()).to_be_visible()

    # Step 2: Add product to cart
    home_page.open_home_page()
    home_page.enter_product_name(product_name)
    home_page.click_search()
    search_results_page.select_product(product_name)
    
    expected_name = product_page.get_product_name()
    product_page.add_to_cart()
    expect(product_page.get_any_alert_message()).to_be_visible()

    # Step 3: Click on Cart button to open toggle box
    product_page.click_cart_button()
    
    # Step 4: Click name link in the toggle box
    product_page.click_cart_name_link()

    # Validation: Navigate to PDP
    expect(product_page.lbl_product_name).to_be_visible(timeout=10000)
    actual_name = product_page.get_product_name()
    assert expected_name in actual_name, messages.PDP_PRODUCT_NAME_MISMATCH.format(
        expected=expected_name, actual=actual_name
    )
