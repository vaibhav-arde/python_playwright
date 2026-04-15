import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.product_comparison_page import ProductComparisonPage
from pages.search_results_page import SearchResultsPage
from utils.constants import UIRoutes
from utils.messages import COMPARE_SUCCESS
from utils.data_loader import read_json_data


@pytest.mark.regression
@pytest.mark.parametrize(
    "product_name, expected_tooltip", read_json_data("test_data/comparedata.json")
)
def test_product_comparison(page, product_name, expected_tooltip):
    """Verify that a product can be added to comparison and the comparison page loads correctly."""

    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    # ===== Step 1 & 2: Search for product =====
    home_page.enter_product_name(product_name)
    home_page.click_search()

    # Verify search results page is displayed
    expect(search_results_page.get_search_results_page_header()).to_be_visible()

    # ===== Step 3: Click on the product from search results =====
    product_page = search_results_page.select_product(product_name)
    assert product_page is not None, f"Product '{product_name}' was not found in search results."

    # ===== Step 4: ER-1 — Validate tooltip on hover =====
    product_page.hover_compare_button()

    actual_tooltip = product_page.get_compare_button_tooltip()
    assert (
        actual_tooltip == expected_tooltip
    ), f"ER-1 FAILED: Expected tooltip '{expected_tooltip}', but got '{actual_tooltip}'"

    # ===== Step 5: Click 'Compare this Product' =====
    product_page.click_compare_button()

    # ===== Step 6: ER-2 — Validate success message =====
    expected_success_msg = COMPARE_SUCCESS.format(product_name=product_name)
    actual_success_msg = product_page.get_compare_success_message()

    assert expected_success_msg in actual_success_msg, (
        f"ER-2 FAILED: Expected message containing '{expected_success_msg}', "
        f"but got '{actual_success_msg}'"
    )

    # ===== Step 7: ER-3 — Click 'product comparison' link from success message =====
    product_page.click_product_comparison_link()

    # ===== Step 8: ER-3 — Validate Product Comparison page =====
    comparison_page = ProductComparisonPage(page)

    # Assert the URL contains the comparison route
    expect(page).to_have_url(
        re.compile(re.escape(UIRoutes.COMPARISON)),
    )

    # Assert the page heading is 'Product Comparison'
    expect(comparison_page.get_page_heading()).to_be_visible()

    # Assert the added product is displayed in the comparison table
    expect(comparison_page.get_product_name_in_table(product_name)).to_be_visible()
