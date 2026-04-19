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
@pytest.mark.parametrize(("product_name",), read_json_data("test_data/comparedata.json"))
def test_validate_success_message_after_adding_product_for_comparison(page, product_name):
    """TC_PC_013 — Validate the success message displayed after adding a product for comparison."""
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    # ===== Step 1 & 2: Search for the product =====
    home_page.enter_product_name(product_name)
    home_page.click_search()

    expect(search_results_page.get_search_results_page_header()).to_be_visible()

    # ===== Step 3: Open the Product Display Page =====
    product_page = search_results_page.select_product(product_name)
    assert product_page is not None

    expect(product_page.get_product_header()).to_have_text(product_name)

    # ===== Step 4: Click 'Compare this Product' =====
    product_page.click_compare_button()

    # ===== ER-1: Validate success message text =====
    expected_success_msg = COMPARE_SUCCESS.format(product_name=product_name)
    actual_success_msg = product_page.get_compare_success_message()
    assert expected_success_msg in actual_success_msg

    # ===== ER-2: Click the Product Name link in the success message =====
    # The link navigates back to the product's own display page.
    expect(product_page.get_product_name_link_in_success_message(product_name)).to_be_visible()
    product_page.click_product_name_link_in_success_message(product_name)

    # Verify the user is taken to the Product Display Page
    expect(product_page.get_product_header()).to_have_text(product_name)

    # ===== ER-3: Click 'Compare this Product' again to get fresh success message =====
    product_page.click_compare_button()
    product_page.get_compare_success_message()  # wait for the alert to appear

    # Click the 'product comparison' link in the success message
    product_page.click_product_comparison_link()

    # Verify the user is taken to the Product Comparison page
    comparison_page = ProductComparisonPage(page)
    expect(page).to_have_url(re.compile(re.escape(UIRoutes.COMPARISON)))
    expect(comparison_page.get_page_heading()).to_be_visible()
