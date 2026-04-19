import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.product_comparison_page import ProductComparisonPage
from pages.search_results_page import SearchResultsPage
from utils.constants import UIRoutes
from utils.data_loader import read_json_data
from utils.messages import COMPARE_SUCCESS


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    ("product_name_1", "product_name_2"),
    read_json_data("test_data/comparedata_two_products.json"),
)
def test_validate_product_comparison_page_with_two_products(page, product_name_1, product_name_2):
    """TC_PC_015 — Validate the Product Comparison page when two products are added."""
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    # ===== Step 1 & 2: Search for the first product =====
    home_page.enter_product_name(product_name_1)
    home_page.click_search()

    expect(search_results_page.get_search_results_page_header()).to_be_visible()

    # ===== Step 3: Click 'Compare this Product' for the first product =====
    search_results_page.click_compare_button(product_name_1)

    # Wait for success message and verify its text
    expected_success_msg_1 = COMPARE_SUCCESS.format(product_name=product_name_1)
    actual_success_msg_1 = search_results_page.get_compare_success_message()
    assert expected_success_msg_1 in actual_success_msg_1

    # ===== Step 4 & 5: Search for the second product =====
    home_page.enter_product_name(product_name_2)
    home_page.click_search()

    expect(search_results_page.get_search_results_page_header()).to_be_visible()

    # ===== Step 6: Click 'Compare this Product' for the second product =====
    search_results_page.click_compare_button(product_name_2)

    # Wait for success message and verify its text
    expected_success_msg_2 = COMPARE_SUCCESS.format(product_name=product_name_2)
    actual_success_msg_2 = search_results_page.get_compare_success_message()
    assert expected_success_msg_2 in actual_success_msg_2

    # ===== Step 7: Click 'product comparison' link from the success message =====
    search_results_page.click_product_comparison_link()

    # ===== Step 8: Validate Product Comparison page with two products (ER-1) =====
    comparison_page = ProductComparisonPage(page)

    # Verify we are on the Product Comparison page
    expect(page).to_have_url(re.compile(re.escape(UIRoutes.COMPARISON)))
    expect(comparison_page.get_page_heading()).to_be_visible()

    # Verify both product names are displayed in the comparison table
    expect(comparison_page.get_product_name_in_table(product_name_1)).to_be_visible()
    expect(comparison_page.get_product_name_in_table(product_name_2)).to_be_visible()

    # Verify both product images are displayed
    expect(comparison_page.get_product_image_in_table(product_name_1)).to_be_visible()
    expect(comparison_page.get_product_image_in_table(product_name_2)).to_be_visible()

    # Verify two price cells are displayed — one per product column
    expect(comparison_page.get_all_price_cells_in_table()).to_have_count(2)

    # Verify two 'Add to Cart' buttons are displayed — one per product column
    expect(comparison_page.get_add_to_cart_button_in_table()).to_have_count(2)

    # Verify two 'Remove' links are displayed — one per product column
    expect(comparison_page.get_remove_link_in_table()).to_have_count(2)
