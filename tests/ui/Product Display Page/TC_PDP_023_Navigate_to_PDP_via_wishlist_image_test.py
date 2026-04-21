import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from pages.wishlist_page import WishListPage
from pages.login_page import LoginPage
from utils.constants import TestData, UIRoutes
from utils.config import Config
from utils import messages

@pytest.mark.ui
@pytest.mark.regression
def test_navigate_to_pdp_via_wishlist_image(page: Page):
    """
    Test Case ID: TC_PDP_023
    Validate navigating to the Product Display page by using the Product image in the 'Wish List' page
    """
    home_page = HomePage(page)
    login_page = LoginPage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)
    wishlist_page = WishListPage(page)

    product_name = TestData.PRODUCT_NAME_IMAC

    # Step 1: Login
    home_page.open_home_page()
    home_page.click_my_account()
    home_page.click_login()
    login_page.login(Config.email, Config.password)

    # Step 2: Add product to wishlist
    home_page.enter_product_name(product_name)
    home_page.click_search()
    search_results_page.select_product(product_name)
    product_page.click_add_to_wishlist()
    expect(product_page.get_confirmation_message()).to_be_visible()

    # Step 3: Go to Wish List page
    page.goto(UIRoutes.WISHLIST)
    expect(wishlist_page.lbl_heading).to_be_visible()

    # Step 4: Click image in Wish List
    wishlist_page.click_product_image(product_name)

    # Validate navigation to PDP
    expect(product_page.lbl_product_name).to_be_visible()
    actual_name = product_page.get_product_name()
    assert actual_name == product_name, messages.PDP_PRODUCT_NAME_MISMATCH.format(expected=product_name, actual=actual_name)
