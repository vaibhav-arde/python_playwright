import re
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.product_comparison_page import ProductComparisonPage
from pages.search_results_page import SearchResultsPage
from utils.constants import UIRoutes
from utils.data_loader import load_json_file
from utils.messages import COMPARE_SUCCESS, REMOVE_SUCCESS


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "product_names",
    [
        *load_json_file("test_data/product_comparison.json")["one_product"],
        *load_json_file("test_data/product_comparison.json")["two_products"],
    ],
)
def test_validate_remove_product_from_comparison_page(page, product_names):
    """TC_PC_021 — Validate removing products from the 'Product Comparison' page."""
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    comparison_page = ProductComparisonPage(page)

    # ===== Steps 1-3: Search and add product(s) to comparison =====
    for product in product_names:
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

    # Verify we are on the Product Comparison page
    expect(page).to_have_url(re.compile(re.escape(UIRoutes.COMPARISON)))
    expect(comparison_page.get_page_heading()).to_be_visible()

    # ===== Step 5: Click 'Remove' button of the Product(s) from the 'Product Comparison' page =====
    for product in product_names:
        comparison_page.click_remove_for_product(product)

        # Verify success message for removal (Validate ER-1)
        expect(comparison_page.success_message).to_contain_text(REMOVE_SUCCESS)

        # Verify the removed product is no longer in the table
        expect(comparison_page.get_product_name_in_table(product)).to_have_count(0)

    # If all products were removed, verify the empty comparison message
    expect(comparison_page.empty_comparison_text).to_be_visible()
