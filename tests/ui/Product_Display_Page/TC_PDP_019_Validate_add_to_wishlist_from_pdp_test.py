import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from pages.wishlist_page import WishListPage
from pages.registration_page import RegistrationPage
from utils.constants import TestData
from utils import messages
from utils.random_test_data import RandomTestData


@pytest.mark.ui
@pytest.mark.regression
def test_validate_add_to_wishlist_from_pdp(page: Page):
    """
    Test Case ID: TC_PDP_019
    Validate adding the product to 'Wish List' from the Product Display page
    """
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)
    wishlist_page = WishListPage(page)
    registration_page = RegistrationPage(page)

    product_name = TestData.PRODUCT_NAME_IMAC

    # Step 1: Register a new account to ensure active session
    home_page.open_home_page()
    home_page.click_my_account()
    home_page.click_register()

    # Use the POM helper and method to complete registration dynamically
    unique_user = RandomTestData.get_user()
    registration_page.complete_registration(unique_user)
    expect(registration_page.get_confirmation_msg()).to_be_visible()

    # Step 2: Search for a product
    home_page.open_home_page()
    home_page.enter_product_name(product_name)
    home_page.click_search()

    product_in_results = search_results_page.is_product_exist(product_name)
    assert product_in_results is not None, messages.SEARCH_RESULT_PRODUCT_NOT_FOUND.format(
        keyword=product_name
    )

    expected_product_name = search_results_page.get_text(product_in_results).strip()
    search_results_page.select_product(expected_product_name)

    # Step 4: Add to Wish List
    product_page.click_add_to_wishlist()

    # Validate ER-1: Success message
    success_alert = product_page.get_any_alert_message()
    expect(success_alert).to_be_visible(timeout=10000)

    actual_msg = product_page.get_text(success_alert)
    assert (
        messages.SUCCESS_ALERT_KEYWORD in actual_msg
    ), f"Expected success message but got: {actual_msg}"
    assert expected_product_name in actual_msg, messages.PDP_PRODUCT_NAME_MISMATCH.format(
        expected=expected_product_name, actual=actual_msg
    )

    # Step 5: Click 'wish list' link in success message
    product_page.click_wishlist_link_on_success_msg()

    # Validate ER-2: Navigation to Wish List page
    expect(wishlist_page.lbl_heading).to_be_visible(timeout=10000)

    # Validate product presence in wishlist
    row = wishlist_page.get_product_row_by_name(expected_product_name)
    expect(row).to_be_visible(), f"Product {expected_product_name} not found in Wish List"
