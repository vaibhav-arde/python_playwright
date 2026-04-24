import re
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.registration_page import RegistrationPage
from pages.search_results_page import SearchResultsPage
from utils.messages import (
    ERR_PRODUCT_NOT_FOUND,
    MY_ACCOUNT_HEADING,
    MY_WISHLIST_HEADING,
)
from utils.constants import TestData, UIRoutes
from utils.random_test_data import RandomTestData


@pytest.mark.ui
def test_validate_multiple_products_wishlist_page(page):
    """
    TC_WL_017: Validate adding the multiple products to the 'My Wish List' page
    """
    home_page = HomePage(page)
    my_account_page = MyAccountPage(page)
    registration_page = RegistrationPage(page)
    search_results_page = SearchResultsPage(page)

    # Pre-requisite: Create a fresh account
    # Note: Using dynamic registration to ensure a clean session and valid login.
    home_page.click_my_account()
    home_page.click_register()
    user_data = RandomTestData.get_user()
    registration_page.complete_registration(user_data)
    registration_page.click_continue()

    # Pre-requisite: Add multiple products to 'My Wish List' page
    products_to_add = [TestData.PRODUCT_IMAC, TestData.PRODUCT_MACBOOK]
    product_details = {}

    for product_name in products_to_add:
        home_page.click_logo()
        home_page.enter_product_name(product_name)
        home_page.click_search()
        product_page = search_results_page.select_product(product_name)
        assert product_page is not None, ERR_PRODUCT_NOT_FOUND.format(product_name=product_name)

        # Capture product details from PDP to verify later in the wishlist table
        product_details[product_name] = {
            "model": product_page.get_product_model_value(),
            "stock": product_page.get_product_stock_value(),
            "price": product_page.get_product_unit_price_value(),
        }

        product_page.add_product_to_wishlist()
        expect(product_page.get_confirmation_message()).to_be_visible()

    # Test Step 1: Click on 'Modify your wish list' option
    home_page.click_my_account()
    home_page.click_my_account_option()
    wishlist_page = my_account_page.click_modify_wishlist_option()

    # Acceptance Criteria:
    # 1. User should be taken to 'My Wish List' page
    expect(page).to_have_url(re.compile(rf".*{re.escape(UIRoutes.WISHLIST)}.*"))
    expect(wishlist_page.get_wishlist_page_heading()).to_have_text(MY_WISHLIST_HEADING)

    # 2. All multiple products added are displayed with correct details
    for product_name in products_to_add:
        expect(wishlist_page.is_product_in_wishlist(product_name)).to_be_visible()

        details = product_details[product_name]
        expect(wishlist_page.get_product_name_link(product_name)).to_have_text(product_name)
        expect(wishlist_page.get_product_model(product_name)).to_have_text(details["model"])
        expect(wishlist_page.get_product_stock(product_name)).to_have_text(details["stock"])
        expect(wishlist_page.get_product_unit_price(product_name)).to_have_text(details["price"])

        # 3. Verify all action options are visible for each product
        expect(wishlist_page.get_product_image_link(product_name)).to_be_visible()
        expect(wishlist_page.get_add_to_cart_button(product_name)).to_be_visible()
        expect(wishlist_page.get_remove_link(product_name)).to_be_visible()

    # 4. Verify interactivity (Image link, Name link, and Continue button)
    target_product = products_to_add[0]

    # Image link navigation
    product_page = wishlist_page.click_product_image(target_product)
    expect(product_page.get_product_page_heading()).to_have_text(target_product)
    page.go_back()
    page.wait_for_load_state()

    # Name link navigation
    product_page = wishlist_page.click_product_name(target_product)
    expect(product_page.get_product_page_heading()).to_have_text(target_product)
    page.go_back()
    page.wait_for_load_state()

    # Continue button navigation
    my_account_page = wishlist_page.click_continue_button()
    expect(my_account_page.get_my_account_page_heading()).to_have_text(MY_ACCOUNT_HEADING)
    expect(page).to_have_url(re.compile(rf".*{re.escape(UIRoutes.MY_ACCOUNT)}.*"))
