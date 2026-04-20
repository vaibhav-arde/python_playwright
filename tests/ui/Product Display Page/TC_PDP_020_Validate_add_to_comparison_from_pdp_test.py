import pytest
import re
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from pages.product_comparison_page import ProductComparisonPage
from utils.constants import TestData
from utils import messages

@pytest.mark.ui
@pytest.mark.regression
def test_validate_add_to_comparison_from_pdp(page: Page):
    """
    Test Case ID: TC_PDP_020
    Validate adding the product for comparison from the Product Display page
    """
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)
    comparison_page = ProductComparisonPage(page)

    product_name = TestData.PRODUCT_NAME_IMAC

    home_page.enter_product_name(product_name)
    home_page.click_search()

    product_in_results = search_results_page.is_product_exist(product_name)
    assert product_in_results is not None, messages.SEARCH_RESULT_PRODUCT_NOT_FOUND.format(keyword=product_name)

    expected_product_name = search_results_page.get_text(product_in_results).strip()
    search_results_page.select_product(expected_product_name)

    # Step 4: Add to Comparison
    product_page.click_compare()

    # Validate ER-1: Success message
    success_alert = product_page.any_alert_msg.first
    expect(success_alert).to_be_visible(timeout=10000)
    actual_msg = product_page.get_text(success_alert)
    assert expected_product_name in actual_msg, f"Success message should mention {expected_product_name}"

    # Step 5: Click 'product comparison' link
    # Using case-insensitive regex for the link name 
    success_alert.get_by_role("link", name=re.compile(r"product comparison", re.IGNORECASE)).click()

    # Validate ER-2: Navigation to Comparison page
    expect(comparison_page.lbl_heading).to_be_visible(timeout=10000)
    assert comparison_page.is_product_in_comparison(expected_product_name), \
        f"Product {expected_product_name} should be in the comparison table"
