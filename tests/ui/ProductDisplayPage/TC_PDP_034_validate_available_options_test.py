# tests/ui/ProductDisplayPage/TC_PDP_034_validate_available_options_test.py

"""
TC_PDP_034
(TS_007) Product Display Page

Validate all the extra available options in the Product Display page

Steps:
1. Open the Application URL and Login
2. Enter any existing Product name into Search text box
3. Click search icon
4. Click Product displayed in Search results
5. Validate all available options on Product Display Page

Test Data:
Product Name: Apple Cinema 30"
"""

import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from pages.registration_page import RegistrationPage
from utils.constants import TestData
from utils.random_test_data import RandomTestData


@pytest.mark.ui
@pytest.mark.regression
def test_validate_available_options(page: Page):
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)
    registration_page = RegistrationPage(page)


    # Step 1: Open Application URL and Register new account
    # User is auto-logged in after successful registration
    home_page.open_home_page()
    home_page.click_my_account()
    home_page.click_register()

    unique_user = RandomTestData.get_user()
    registration_page.complete_registration(unique_user)

    # Navigate back to Home Page
    home_page.open_home_page()

    # Step 2: Enter Product Name
    home_page.enter_product_name(TestData.PRODUCT_NAME_APPLE_CINEMA_30)

    # Step 3: Click Search icon
    home_page.click_search()

    # Step 4: Click Product displayed in Search Results
    search_results_page.select_product(TestData.PRODUCT_NAME_APPLE_CINEMA_30)

    # Step 5: Validate Available Options
    # Explicit expectation in test script as per user requirement
    expect(product_page.lbl_product_name).to_be_visible()

    product_page.verify_available_options()
