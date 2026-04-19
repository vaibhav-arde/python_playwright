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
    ("product_name",),
    read_json_data("test_data/comparedata.json"),
)
def test_validate_same_product_added_twice_to_comparison(page, product_name):
    """TC_PC_016 — Validate the 'Product Comparison' page when the same product is added twice."""
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    comparison_page = ProductComparisonPage(page)

    # ===== Step 1 & 2: Search for the product (First time) =====
    home_page.enter_product_name(product_name)
    home_page.click_search()
    expect(search_results_page.get_search_results_page_header()).to_be_visible()

    # ===== Step 3: Click 'Compare this Product' for the first time =====
    search_results_page.click_compare_button(product_name)

    # Wait for success message and verify its text
    expected_success_msg = COMPARE_SUCCESS.format(product_name=product_name)
    actual_success_msg = search_results_page.get_compare_success_message()
    assert expected_success_msg in actual_success_msg

    # ===== Step 4 & 5: Search for the same product again =====
    home_page.enter_product_name(product_name)
    home_page.click_search()
    expect(search_results_page.get_search_results_page_header()).to_be_visible()

    # ===== Step 6: Click 'Compare this Product' for the second time =====
    search_results_page.click_compare_button(product_name)

    # Wait for success message and verify its text
    actual_success_msg_2 = search_results_page.get_compare_success_message()
    assert expected_success_msg in actual_success_msg_2

    # ===== Step 7: Click 'product comparison' link from the success message =====
    search_results_page.click_product_comparison_link()

    # ===== Step 8: Validate Product Comparison page (Validate ER-1) =====
    # Verify we are on the Product Comparison page
    expect(page).to_have_url(re.compile(re.escape(UIRoutes.COMPARISON)))
    expect(comparison_page.get_page_heading()).to_be_visible()

    # Acceptance Criteria: The product should be displayed only ONCE

    # Verify the product name is displayed in the comparison table
    expect(comparison_page.get_product_name_in_table(product_name)).to_have_count(1)

    # Verify the product image is displayed exactly once
    expect(comparison_page.get_product_image_in_table(product_name)).to_have_count(1)

    # Verify only one price cell is displayed — confirming one product column
    expect(comparison_page.get_all_price_cells_in_table()).to_have_count(1)

    # Verify only one 'Add to Cart' button is displayed
    expect(comparison_page.get_add_to_cart_button_in_table()).to_have_count(1)

    # Verify only one 'Remove' link is displayed
    expect(comparison_page.get_remove_link_in_table()).to_have_count(1)
