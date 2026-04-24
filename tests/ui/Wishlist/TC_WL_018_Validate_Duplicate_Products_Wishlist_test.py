import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from pages.search_results_page import SearchResultsPage
from utils.messages import (
    ERR_PRODUCT_NOT_FOUND,
    MY_WISHLIST_HEADING,
    ERR_DUPLICATE_PRODUCT_IN_WISHLIST,
)
from utils.constants import TestData
from utils.random_test_data import RandomTestData


@pytest.mark.ui
def test_validate_duplicate_products_wishlist_page(page):
    """
    TC_WL_018: Validate adding duplicate products to 'My Wish List' page
    """
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)
    search_results_page = SearchResultsPage(page)

    # Pre-requisite: Open the Application URL and login
    # Note: Using dynamic registration to ensure a clean session and valid login.
    home_page.click_my_account()
    home_page.click_register()
    user_data = RandomTestData.get_user()
    registration_page.complete_registration(user_data)
    registration_page.click_continue()

    # Test Step 1: Enter any existing Product name into the Search text box field
    product_name = TestData.PRODUCT_IMAC
    home_page.enter_product_name(product_name)

    # Test Step 2: Click on the button having search icon
    home_page.click_search()

    # Test Step 3: Click on the Product displayed in the Search results
    product_page = search_results_page.select_product(product_name)
    assert product_page is not None, ERR_PRODUCT_NOT_FOUND.format(product_name=product_name)

    # Test Step 4: Click on 'Add to Wish List' option in the displayed 'Product Display' page
    product_page.add_product_to_wishlist()
    expect(product_page.get_confirmation_message()).to_be_visible()

    # Test Step 5: Repeat Step 4 multiple times (Adding the same product 2 more times)
    for _ in range(3):
        product_page.add_product_to_wishlist()
        expect(product_page.get_confirmation_message()).to_be_visible()

    # Test Step 6: Click on 'wish list!' link from the Success message
    wishlist_page = product_page.click_wishlist_link_in_message()

    # Acceptance Criteria:
    # 1. User should be taken to 'My Wish List' page
    expect(wishlist_page.get_wishlist_page_heading()).to_have_text(MY_WISHLIST_HEADING)

    # 2. Only one product should be displayed without any duplications in this page.
    # We verify that the count of entries for this product in the wishlist table is exactly 1.
    product_count = wishlist_page.get_product_count_in_wishlist(product_name)
    assert product_count == 1, ERR_DUPLICATE_PRODUCT_IN_WISHLIST.format(
        product_name=product_name, product_count=product_count
    )
