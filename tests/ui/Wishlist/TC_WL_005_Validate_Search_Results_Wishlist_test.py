import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from pages.search_results_page import SearchResultsPage
from utils.constants import TestData
from utils.messages import SUCCESS_WISH_LIST
from utils.random_test_data import RandomTestData


@pytest.mark.sanity
@pytest.mark.ui
def test_add_search_results_product_to_wishlist(page):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)
    search_results_page = SearchResultsPage(page)

    # Pre-requisite: Register new user (ensures dynamic login and clean state)
    home_page.click_my_account()
    home_page.click_register()

    user_data = RandomTestData.get_user()
    registration_page.complete_registration(user_data)

    # Step 1 & 2: Search for product
    product_name = TestData.PRODUCT_IMAC
    home_page.enter_product_name(product_name)
    home_page.click_search()

    # Step 3: Click 'Add to Wish List' on the product displayed in Search Results
    search_results_page.add_product_to_wishlist(product_name)

    # Validate ER-1: Success message
    success_msg_locator = search_results_page.get_success_message()
    expected_msg = SUCCESS_WISH_LIST.format(product_name=product_name)
    expect(success_msg_locator).to_contain_text(expected_msg)

    # Step 4: Click on the 'wish list!' link in the displayed success message
    wishlist_page = search_results_page.click_wishlist_link_in_success_message()

    # Validate ER-2: Product successfully displayed in My Wish List
    expect(wishlist_page.is_product_in_wishlist(product_name)).to_be_visible()
