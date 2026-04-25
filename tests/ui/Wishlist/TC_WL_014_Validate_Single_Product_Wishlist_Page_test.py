import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.registration_page import RegistrationPage
from pages.search_results_page import SearchResultsPage
from utils.messages import ERR_PRODUCT_NOT_FOUND, MY_ACCOUNT_HEADING
from utils.constants import TestData, UIRoutes, WishlistColumnNames
from utils.random_test_data import RandomTestData


@pytest.mark.ui
@pytest.mark.critical
def test_validate_single_product_wishlist_page(page):
    home_page = HomePage(page)
    my_account_page = MyAccountPage(page)
    registration_page = RegistrationPage(page)
    search_results_page = SearchResultsPage(page)

    # Pre-requisite: Create a fresh account and add one product to wishlist
    product_name = TestData.PRODUCT_IMAC
    home_page.click_my_account()
    home_page.click_register()

    user_data = RandomTestData.get_user()
    registration_page.complete_registration(user_data)
    registration_page.click_continue()

    home_page.click_logo()
    home_page.enter_product_name(product_name)
    home_page.click_search()
    product_page = search_results_page.select_product(product_name)
    assert product_page is not None, ERR_PRODUCT_NOT_FOUND.format(product_name=product_name)

    expected_model = product_page.get_product_model_value()
    expected_stock = product_page.get_product_stock_value()
    expected_unit_price = product_page.get_product_unit_price_value()

    product_page.add_product_to_wishlist()
    expect(product_page.get_confirmation_message()).to_be_visible()

    home_page.click_my_account()
    home_page.click_my_account_option()

    # Step 1: Click on 'Modify your wish list' option
    wishlist_page = my_account_page.click_modify_wishlist_option()

    # Validate ER-1 and ER-2: Proper product details should be displayed
    expected_headers = [
        WishlistColumnNames.IMAGE,
        WishlistColumnNames.PRODUCT_NAME,
        WishlistColumnNames.MODEL,
        WishlistColumnNames.STOCK,
        WishlistColumnNames.UNIT_PRICE,
        WishlistColumnNames.ACTION,
    ]
    assert wishlist_page.get_wishlist_table_headers() == expected_headers
    expect(wishlist_page.get_product_image_link(product_name)).to_be_visible()
    expect(wishlist_page.get_product_name_link(product_name)).to_have_text(product_name)
    expect(wishlist_page.get_product_model(product_name)).to_have_text(expected_model)
    expect(wishlist_page.get_product_stock(product_name)).to_have_text(expected_stock)
    expect(wishlist_page.get_product_unit_price(product_name)).to_have_text(expected_unit_price)
    expect(wishlist_page.get_add_to_cart_button(product_name)).to_be_visible()
    expect(wishlist_page.get_remove_link(product_name)).to_be_visible()

    product_page = wishlist_page.click_product_image(product_name)
    expect(page).to_have_url(re.compile(rf".*{re.escape(UIRoutes.PRODUCT_DISPLAY)}.*"))
    expect(product_page.get_product_page_heading()).to_have_text(product_name)

    page.go_back()
    page.wait_for_load_state()

    product_page = wishlist_page.click_product_name(product_name)
    expect(page).to_have_url(re.compile(rf".*{re.escape(UIRoutes.PRODUCT_DISPLAY)}.*"))
    expect(product_page.get_product_page_heading()).to_have_text(product_name)

    page.go_back()
    page.wait_for_load_state()

    # Step 2: Click on 'Continue' button
    my_account_page = wishlist_page.click_continue_button()

    # Validate ER-3: User should be taken to 'My Account' page
    expect(page).to_have_url(re.compile(rf".*{re.escape(UIRoutes.MY_ACCOUNT)}.*"))
    expect(my_account_page.get_my_account_page_heading()).to_have_text(MY_ACCOUNT_HEADING)
