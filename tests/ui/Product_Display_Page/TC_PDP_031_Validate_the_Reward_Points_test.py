import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData
from utils.random_test_data import RandomTestData

@pytest.mark.ui
class TestProductDisplayPage:
    """Test suite for Product Display Page (PDP) validations."""

    def test_validate_reward_points(self, page: Page):
        """
        TC_PDP_031: Validate the Reward Points displayed in the Product Display page.

        Steps:
        1. Open Application URL and Register a new account.
        2. Enter product name into the Search text box.
        3. Click on the search icon.
        4. Click on the Product displayed in search results.
        5. Verify the 'Reward Points' are displayed.
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

        # 5. Validate Reward Points
        reward_points = product_page.get_reward_points()

        # Validate that reward points are displayed (not empty)
        assert reward_points != "", f"Reward points should be displayed for product {product_name}"
        print(f"Verified reward points for {product_name}: {reward_points}")
