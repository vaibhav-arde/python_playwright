import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from pages.search_results_page import SearchResultsPage
from utils.constants import TestData, UIRoutes
from utils.messages import ERR_PRODUCT_NOT_FOUND, MY_WISHLIST_HEADING
from utils.random_test_data import RandomTestData


@pytest.mark.ui
def test_navigate_to_wishlist_from_success_message(page):
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

    # Step 3: Click on the Product displayed in Search Results
    product_page = search_results_page.select_product(product_name)
    assert product_page is not None, ERR_PRODUCT_NOT_FOUND.format(product_name=product_name)

    # Step 4: Add displayed Product to Wish List
    product_page.add_product_to_wishlist()

    # Step 5: Click the 'wish list!' link in the success message
    wishlist_page = product_page.click_wishlist_link_in_message()

    # Validate ER-1: User should be taken to My Wish List page
    expect(page).to_have_url(re.compile(rf".*{re.escape(UIRoutes.WISHLIST)}.*"))
    expect(wishlist_page.get_wishlist_page_heading()).to_have_text(MY_WISHLIST_HEADING)
