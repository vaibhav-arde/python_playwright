import re
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.product_comparison_page import ProductComparisonPage
from pages.search_results_page import SearchResultsPage
from utils.constants import UIRoutes
from utils.data_loader import load_json_file
from utils.messages import (
    COMPARISON_PAGE_HEADING,
    COMPARE_SUCCESS,
)


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "product_names",
    load_json_file("test_data/product_comparison.json")["one_product"],
)
def test_validate_comparison_functionality_across_environments(page, product_names):
    """TC_PC_024 — Validate the 'Product Comparison' functionality in all the supported environments."""
    product = product_names[0]
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    comparison_page = ProductComparisonPage(page)

    # ===== Step 1: Search for the product =====
    home_page.enter_product_name(product)
    home_page.click_search()
    expect(search_results_page.get_search_results_page_header()).to_be_visible()

    # ===== Step 2: Select 'Compare this Product' option =====
    search_results_page.click_compare_button(product)

    # Verify success message for comparison
    expected_compare_msg = COMPARE_SUCCESS.format(product_name=product)
    actual_compare_msg = search_results_page.get_compare_success_message()
    assert expected_compare_msg in actual_compare_msg

    # ===== Step 3: Click 'Product Comparison' link in the displayed success message =====
    search_results_page.click_product_comparison_link()

    # ===== Step 4: Validate the Comparison Page (Validate ER-1) =====
    # 1. URL Validation
    expect(page).to_have_url(re.compile(re.escape(UIRoutes.COMPARISON)))

    # 2. Page Heading Validation
    expect(comparison_page.get_page_heading()).to_be_visible()
    expect(comparison_page.get_page_heading()).to_have_text(COMPARISON_PAGE_HEADING)

    # 3. Product Presence Validation
    expect(comparison_page.get_product_name_in_table(product)).to_be_visible()
    expect(comparison_page.get_product_image_in_table(product)).to_be_visible()
