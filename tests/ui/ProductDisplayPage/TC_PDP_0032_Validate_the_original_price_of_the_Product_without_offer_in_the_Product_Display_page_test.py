import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData, UIPricing
from utils.random_test_data import RandomTestData


@pytest.mark.ui
class TestProductDisplayPage:
    """Test suite for Product Display Page (PDP) validations."""

    def test_validate_original_price_without_offer(self, page: Page):
        """
        TC_PDP_0032: Validate the original price of the Product without offer in the Product Display page.

        Steps:
        1. Open Application URL and Register a new account.
        2. Enter any existing Product name into the Search text box field.
        3. Click on the button having search icon.
        4. Click on the Product displayed in the Search results.
        5. Check the original price of the Product without offer in the displayed 'Product Display' page.
        """
        home_page = HomePage(page)
        registration_page = RegistrationPage(page)

        # 1. Register a new account to ensure active session
        home_page.open_home_page()
        home_page.click_my_account()
        home_page.click_register()

        unique_user = RandomTestData.get_user()
        registration_page.complete_registration(unique_user)
        expect(registration_page.get_confirmation_msg()).to_be_visible()

        # 2 & 3. Search for Product
        home_page.open_home_page()
        product_name = TestData.PRODUCT_NAME_APPLE_CINEMA_30
        home_page.enter_product_name(product_name)
        home_page.click_search()

        # 4. Select Product from Results
        search_results_page = SearchResultsPage(page)
        search_results_page.select_product(product_name)
        product_page = ProductPage(page)

        # 5. Check the original price of the Product
        # ER: Proper Product Price should be displayed
        expect(product_page.lbl_product_price).to_be_visible()

        price = product_page.get_product_price()

        # Validate that price is not empty and contains a currency symbol
        assert price != TestData.EMPTY_VALUE, "Product price should not be empty"
        assert any(
            symbol in price for symbol in UIPricing.CURRENCY_SYMBOLS
        ), f"Price '{price}' does not contain a valid currency symbol"


