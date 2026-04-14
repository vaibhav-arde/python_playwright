import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData

# Removed local PRODUCT_NAME in favor of centralized TestData.PRODUCT_NAME_IMAC

def test_validate_name_brand_product_code_displayed(page: Page):
    """
    Test Case ID: TC_PDP_002
    Validate that Product Name, Brand and Product Code are displayed in the Product Display Page
    """
    # Initialize Page Objects
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)

    # Note: conftest.py's navigate_to_base_url fixture already navigates to the base URL
    
    # Step 1: Enter any existing Product name into the Search text box field
    home_page.enter_product_name(TestData.PRODUCT_NAME_IMAC)

    # Step 2: Click on the button having search icon
    home_page.click_search()

    # Step 3: Click on the Product displayed in the Search results
    search_results_page.select_product(TestData.PRODUCT_NAME_IMAC)

    # Step 4: Check the Product Name, Brand and Product Code in the displayed Product Display Page
    
    # Validate ER-1: Proper Product Name should be displayed
    expect(product_page.lbl_product_name).to_be_visible()
    actual_product_name = product_page.get_product_name()
    assert actual_product_name == TestData.PRODUCT_NAME_IMAC, f"Expected Product Name '{TestData.PRODUCT_NAME_IMAC}', but got '{actual_product_name}'"

    # Validate ER-1: Proper Brand should be displayed
    expect(product_page.lbl_product_brand).to_be_visible()
    actual_brand = product_page.get_product_brand()
    assert actual_brand != "", "Product Brand should not be empty"

    # Validate ER-1: Proper Product Code should be displayed
    expect(product_page.lbl_product_code).to_be_visible()
    actual_product_code = product_page.get_product_code()
    assert actual_product_code != "", "Product Code should not be empty"
