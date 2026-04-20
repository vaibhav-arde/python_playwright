import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from pages.wishlist_page import WishListPage
from utils.constants import TestData
from utils import messages

@pytest.mark.ui
@pytest.mark.regression
def test_validate_add_to_wishlist_from_pdp(page: Page):
    """
    Test Case ID: TC_PDP_019
    Validate adding the product to 'Wish List' from the Product Display page

    Steps:
        1. Open the Application URL and Login (handled by fixtures)
        2. Search for a product (iMac)
        3. Select the product from search results
        4. Click 'Add to Wish List'
        5. Click 'wish list' link in success message

    Expected Result:
        1. Success message 'Success: You have added Product Name to your wish list!' is displayed
        2. User should be taken to 'Wish List' page and the product added is displayed
    """
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)
    wishlist_page = WishListPage(page)

    product_name = TestData.PRODUCT_NAME_IMAC

    from pages.login_page import LoginPage
    from utils.config import Config
    login_page = LoginPage(page)
    
    # Step 1: Login
    home_page.click_my_account()
    home_page.click_login()
    login_page.login(Config.email, Config.password)

    # Step 2: Search for a product
    home_page.enter_product_name(product_name)
    home_page.click_search()

    product_in_results = search_results_page.is_product_exist(product_name)
    assert product_in_results is not None, messages.SEARCH_RESULT_PRODUCT_NOT_FOUND.format(keyword=product_name)

    expected_product_name = search_results_page.get_text(product_in_results).strip()
    search_results_page.select_product(expected_product_name)

    # Step 4: Add to Wish List
    product_page.click_add_to_wishlist()

    # Validate ER-1: Success message
    success_alert = product_page.get_confirmation_message()
    expect(success_alert).to_be_visible()
    actual_msg = product_page.get_text(success_alert)
    assert expected_product_name in actual_msg, f"Success message should mention {expected_product_name}"

    # Step 5: Click 'wish list' link in success message
    # The link is typically inside the success alert
    success_alert.get_by_role("link", name="Wish List").click()

    # Validate ER-2: Navigation to Wish List page
    # Use explicit wait for the heading to be visible to handle redirect
    expect(wishlist_page.lbl_heading).to_be_visible(timeout=10000)

    row = wishlist_page.get_product_row_by_name(expected_product_name)
    expect(row).to_be_visible(), f"Product {expected_product_name} not found in Wish List"
