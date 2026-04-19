import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.product_comparison_page import ProductComparisonPage
from pages.search_results_page import SearchResultsPage
from utils.constants import UIRoutes
from utils.data_loader import load_json_file
from utils.messages import COMPARE_SUCCESS


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "product_names",
    load_json_file("test_data/product_comparison.json")["five_products"],
)
def test_validate_max_four_products_in_comparison(page, product_names):
    """TC_PC_019 — Validate that only the latest four products are kept in comparison."""
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    comparison_page = ProductComparisonPage(page)

    # Identify the first product and the latest four
    first_product = product_names[0]
    latest_four_products = product_names[1:]

    # ===== Steps 1-3 repeated five times: Search and add five products =====
    for product in product_names:
        home_page.enter_product_name(product)
        home_page.click_search()
        expect(search_results_page.get_search_results_page_header()).to_be_visible()

        search_results_page.click_compare_button(product)

        # Verify success message
        expected_success_msg = COMPARE_SUCCESS.format(product_name=product)
        actual_success_msg = search_results_page.get_compare_success_message()
        assert expected_success_msg in actual_success_msg

    # ===== Step 4: Click 'product comparison' link from the last success message =====
    search_results_page.click_product_comparison_link()

    # ===== Step 5: Validate Product Comparison page (Validate ER-1) =====
    # Verify we are on the Product Comparison page
    expect(page).to_have_url(re.compile(re.escape(UIRoutes.COMPARISON)))
    expect(comparison_page.get_page_heading()).to_be_visible()

    # Acceptance Criteria: First product (iMac) should be REMOVED
    expect(comparison_page.get_product_name_in_table(first_product)).to_have_count(0)
    expect(comparison_page.get_product_image_in_table(first_product)).to_have_count(0)

    # Acceptance Criteria: Latest four products should be DISPLAYED
    for product in latest_four_products:
        expect(comparison_page.get_product_name_in_table(product)).to_be_visible()
        expect(comparison_page.get_product_image_in_table(product)).to_be_visible()

    # Verify exactly four columns/products are displayed
    expect(comparison_page.get_all_price_cells_in_table()).to_have_count(4)
    expect(comparison_page.get_add_to_cart_button_in_table()).to_have_count(4)
    expect(comparison_page.get_remove_link_in_table()).to_have_count(4)
