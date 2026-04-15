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
    "product_name, expected_tooltip", read_json_data("test_data/comparedata.json")
)
def test_add_product_from_search_results_list_view_for_comparison(
    page, product_name, expected_tooltip
):
    """Verify that a product can be added to comparison from search results list view."""

    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    # Step 1 & 2: Search for an existing product
    home_page.enter_product_name(product_name)
    home_page.click_search()

    expect(search_results_page.get_search_results_page_header()).to_be_visible()

    # Step 3: Switch to list view
    search_results_page.click_list_view()

    # Step 4: Hover compare button and validate tooltip
    search_results_page.hover_compare_button(product_name)
    actual_tooltip = search_results_page.get_compare_button_tooltip(product_name)
    assert actual_tooltip == expected_tooltip

    # Step 5: Add product to comparison
    search_results_page.click_compare_button(product_name)

    # Step 6: Validate success message
    expected_success_msg = COMPARE_SUCCESS.format(product_name=product_name)
    actual_success_msg = search_results_page.get_compare_success_message()

    assert expected_success_msg in actual_success_msg

    # Step 7: Open the comparison page
    search_results_page.click_product_comparison_link()

    comparison_page = ProductComparisonPage(page)

    expect(page).to_have_url(
        re.compile(re.escape(UIRoutes.COMPARISON)),
    )
    expect(comparison_page.get_page_heading()).to_be_visible()
    expect(comparison_page.get_product_name_in_table(product_name)).to_be_visible()
