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
def test_navigate_to_pdp_via_wishlist_image(authenticated_page):
    """
    Test Case ID: TC_PDP_023
    Validate navigating to the Product Display page by using the Product image in the 'Wish List' page
    """
    page = authenticated_page
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)
    wishlist_page = WishListPage(page)
    registration_page = RegistrationPage(page)


    # Step 2: Add product to wishlist
    home_page.open_home_page()
    home_page.enter_product_name(TestData.PRODUCT_NAME_IMAC)
    home_page.click_search()
    search_results_page.select_product(TestData.PRODUCT_NAME_IMAC)

    # Capture name for validation
    expected_name = product_page.get_product_name()
    product_page.click_add_to_wishlist()
    expect(product_page.get_any_alert_message()).to_be_visible()

    # Step 3: Go to Wish List page
    home_page.click_wishlist()
    expect(wishlist_page.get_page_heading()).to_be_visible()

    # Step 4: Click on the Product image in the 'Wish List' page
    wishlist_page.click_product_image(expected_name)

    # Validation: Navigate to PDP
    expect(product_page.get_page_heading()).to_be_visible()
    actual_name = product_page.get_product_name()
    assert expected_name in actual_name, messages.PDP_PRODUCT_NAME_MISMATCH.format(
        expected=expected_name, actual=actual_name
    )
