"""
TC_WL_002_Validate adding a product to 'Wish List' page from the Product that is displayed in the 'Related Products' section of 'Product Display' page

Pre-requisites :
Open the Application URL and login

Test Steps :
1. Enter any existing Product name into the Search text box field (iMac)
2. Click on the button having search icon
3. Click on the Product displayed in the Search results
4. Click on 'Add to Wish List' option on a product that is displayed in the 'Related Products' section of displayed 'Product Display' page
5. Click on the 'wish list!' link in the displayed success message

Acceptance Criteria :
1. Success message with text - 'Success: You have added Product Name to your wish list!' should be displayed
2. Product should be successfully displayed in the 'My Wish List' page
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from pages.search_results_page import SearchResultsPage
from utils.constants import TestData
from utils.messages import (
    ERR_PRODUCT_NOT_FOUND,
    ERR_RELATED_PRODUCT_NAME_NOT_FOUND,
    SUCCESS_WISH_LIST,
)
from utils.random_test_data import RandomTestData


@pytest.mark.sanity
@pytest.mark.ui
def test_add_related_product_to_wishlist(page):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)
    search_results_page = SearchResultsPage(page)

    # Pre-requisite: Register new user (ensures dynamic login and clean state)
    home_page.click_my_account()
    home_page.click_register()

    user_data = RandomTestData.get_user()
    registration_page.complete_registration(user_data)

    # Step 1 & 2: Search for product
    home_page.enter_product_name(TestData.PRODUCT_IMAC)
    home_page.click_search()

    # Step 3: Click on the Product in Search Results
    product_page = search_results_page.select_product(TestData.PRODUCT_IMAC)
    assert product_page is not None, ERR_PRODUCT_NOT_FOUND.format(
        product_name=TestData.PRODUCT_IMAC
    )

    # Step 4: Click Add to Wishlist on a Related Product
    added_product_name = product_page.add_related_product_to_wishlist(index=0)
    assert added_product_name, ERR_RELATED_PRODUCT_NAME_NOT_FOUND

    # Validate ER-1: Success message
    success_msg_locator = product_page.get_confirmation_message()
    expected_msg = SUCCESS_WISH_LIST.format(product_name=added_product_name)
    expect(success_msg_locator).to_contain_text(expected_msg)

    # Step 5: Click 'wish list!' link in message
    wishlist_page = product_page.click_wishlist_link_in_message()

    # Validate ER-2: Product successfully displayed in My Wish List
    expect(wishlist_page.is_product_in_wishlist(added_product_name)).to_be_visible()
