import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData, UIPricing
from utils import messages


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.sanity
@pytest.mark.critical
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
    assert any(
        symbol in price for symbol in UIPricing.CURRENCY_SYMBOLS
    ), messages.PDP_PRICE_FORMAT_INCORRECT.format(price=price)
    assert len(price) > 1, messages.PDP_PRODUCT_PRICE_EMPTY

    # ER: Proper Ex Tax should be displayed
    expect(product_page.lbl_product_ex_tax).to_be_visible()
    ex_tax = product_page.get_ex_tax_price()
    assert any(
        symbol in ex_tax for symbol in UIPricing.CURRENCY_SYMBOLS
    ), messages.PDP_EX_TAX_FORMAT_INCORRECT.format(ex_tax=ex_tax)
    assert len(ex_tax) > 1, messages.PDP_EX_TAX_PRICE_EMPTY
