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
    COMPARISON_PAGE_TITLE,
    COMPARE_SUCCESS,
)


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "product_names",
    load_json_file("test_data/product_comparison.json")["one_product"],
)
def test_validate_comparison_page_info(page, product_names):
    """TC_PC_022 — Validate Page Title, Page Heading and Page URL of the 'Product Comparison' page."""
    product = product_names[0]
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    comparison_page = ProductComparisonPage(page)

    # ===== Steps 1-3: Search and add product to comparison =====
    home_page.enter_product_name(product)
    home_page.click_search()
    expect(search_results_page.get_search_results_page_header()).to_be_visible()

    search_results_page.click_compare_button(product)

    # Verify success message for comparison
    expected_compare_msg = COMPARE_SUCCESS.format(product_name=product)
    actual_compare_msg = search_results_page.get_compare_success_message()
    assert expected_compare_msg in actual_compare_msg

    # ===== Step 4: Click 'Product Comparison' link in the displayed success message =====
    search_results_page.click_product_comparison_link()

    # ===== Step 5: Check the Page Title, Page Heading and Page URL (Validate ER-1) =====

    # 1. Validate Page URL
    # We expect the URL to match the comparison route
    expect(page).to_have_url(re.compile(re.escape(UIRoutes.COMPARISON)))

    # 2. Validate Page Title
    expect(page).to_have_title(COMPARISON_PAGE_TITLE)

    # 3. Validate Page Heading
    expect(comparison_page.get_page_heading()).to_have_text(COMPARISON_PAGE_HEADING)
