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
    load_json_file("test_data/product_comparison.json")["four_products"],
)
def test_validate_product_comparison_page_with_four_products(page, product_names):
    """TC_PC_018 — Validate the Product Comparison page when four products are added."""
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    comparison_page = ProductComparisonPage(page)

    # ===== Steps 1-3 repeated four times: Search and add products to comparison =====
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

    # ===== Step 5: Validate Product Comparison page with four products (ER-1) =====
    # Verify we are on the Product Comparison page
    expect(page).to_have_url(re.compile(re.escape(UIRoutes.COMPARISON)))
    expect(comparison_page.get_page_heading()).to_be_visible()

    for product in product_names:
        # Verify product names are displayed in the comparison table
        expect(comparison_page.get_product_name_in_table(product)).to_be_visible()
        # Verify product images are displayed
        expect(comparison_page.get_product_image_in_table(product)).to_be_visible()

    # Verify four price cells are displayed — one per product column
    expect(comparison_page.get_all_price_cells_in_table()).to_have_count(4)

    # Verify four 'Add to Cart' buttons are displayed
    expect(comparison_page.get_add_to_cart_button_in_table()).to_have_count(4)

    # Verify four 'Remove' links are displayed
    expect(comparison_page.get_remove_link_in_table()).to_have_count(4)
