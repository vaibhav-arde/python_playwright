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
    COMPARISON_TABLE_HEADERS,
    COMPARE_SUCCESS,
)


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "product_names",
    load_json_file("test_data/product_comparison.json")["one_product"],
)
def test_validate_comparison_ui(page, product_names):
    """TC_PC_023 — Validate the UI of 'Compare this Product' option and the 'Product Comparison' page."""
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

    # ===== Acceptance Criteria: Validate Proper UI Adhering to the UI Checklist =====

    # 1. Page URL, Title, and Heading
    expect(page).to_have_url(re.compile(re.escape(UIRoutes.COMPARISON)))
    expect(comparison_page.get_page_heading()).to_be_visible()
    expect(comparison_page.get_page_heading()).to_have_text(COMPARISON_PAGE_HEADING)

    # 2. Breadcrumbs
    expect(comparison_page.get_breadcrumb()).to_be_visible()
    expect(comparison_page.get_breadcrumb_home_link()).to_be_visible()
    expect(comparison_page.get_breadcrumb_current_item()).to_be_visible()

    # 3. Comparison Table headers (UI Checklist)
    for header in COMPARISON_TABLE_HEADERS:
        expect(comparison_page.get_row_header(header)).to_be_visible()

    # 4. Product Details in Table
    expect(comparison_page.get_product_name_in_table(product)).to_be_visible()
    expect(comparison_page.get_product_image_in_table(product)).to_be_visible()

    # 5. Action Elements
    expect(comparison_page.get_add_to_cart_button_in_table()).to_be_visible()
    expect(comparison_page.get_remove_link_in_table()).to_be_visible()
