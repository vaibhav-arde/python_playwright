import pytest
from playwright.sync_api import expect, Page
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData

def test_validate_the_product_price(page: Page):
    """
    Test Case ID: TC_PDP_004
    Validate that Product Price and Ex Tax are displayed correctly in the Product Display Page.
    """
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)

    # Step 1-3: Search and Navigate to Product
    home_page.enter_product_name(TestData.PRODUCT_NAME_IMAC)
    home_page.click_search()
    search_results_page.select_product(TestData.PRODUCT_NAME_IMAC)

    # Step 4: Validate Price Display
    # ER: Proper Product Price should be displayed
    expect(product_page.lbl_product_price).to_be_visible()
    price = product_page.get_product_price()
    assert "$" in price or "€" in price or "£" in price, f"Price format incorrect: {price}"
    assert len(price) > 1, "Product price should not be empty"

    # ER: Proper Ex Tax should be displayed
    expect(product_page.lbl_product_ex_tax).to_be_visible()
    ex_tax = product_page.get_ex_tax_price()
    assert "$" in ex_tax or "€" in ex_tax or "£" in ex_tax, f"Ex Tax format incorrect: {ex_tax}"
    assert len(ex_tax) > 1, "Ex Tax price should not be empty"
