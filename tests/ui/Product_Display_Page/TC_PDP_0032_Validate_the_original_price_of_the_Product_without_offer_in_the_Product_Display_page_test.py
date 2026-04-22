"""
1. Enter any existing Product name into the Search text box field -
2. Click on the button having search icon
3. Click on the Product displayed in the Search results
4. Check the original price of the Product without offer in the displayed 'Product Display' page (Validate ER-1)
"""

import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from pages.registration_page import RegistrationPage
from utils.constants import TestData
from utils.random_test_data import RandomTestData


@pytest.mark.ui
@pytest.mark.regression
def test_validate_discounted_price_on_pdp(page: Page):
    """
    TC_PDP_0033
    Validate discounted price (new + old + strike) on PDP
    """

    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)
    registration_page = RegistrationPage(page)

    product_name = TestData.PRODUCT_NAME_APPLE_CINEMA_30

    # Step 1: Register user
    home_page.click_my_account()
    home_page.click_register()

    user = RandomTestData.get_user()
    registration_page.complete_registration(user)
    expect(registration_page.get_confirmation_msg()).to_be_visible()

    # Step 2: Search product
    home_page.open_home_page()
    home_page.enter_product_name(product_name)
    home_page.click_search()

    # Step 3: Open PDP
    search_results_page.select_product(product_name)

    # Step 4: Validate discounted pricing
    product_page.validate_discounted_price()
