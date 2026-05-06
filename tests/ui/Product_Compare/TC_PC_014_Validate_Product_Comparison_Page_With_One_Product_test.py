import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.product_comparison_page import ProductComparisonPage
from pages.search_results_page import SearchResultsPage
from utils.constants import UIRoutes
from utils.data_loader import load_json_file


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(
    "product_names",
    load_json_file("test_data/product_comparison.json")["one_product"],
)
def test_validate_product_comparison_page_with_one_product(page, product_names):
    """TC_PC_014 — Validate the Product Comparison page when one product is added."""
    product_name = product_names[0]
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
    product_page.get_compare_success_message()  # wait for the alert to appear

    # ===== Step 5: Click 'product comparison' link from the success message =====
    product_page.click_product_comparison_link()

    # ===== Step 6: Validate Product Comparison page with one product (ER-1) =====
    comparison_page = ProductComparisonPage(page)

    # Verify we are on the Product Comparison page
    expect(page).to_have_url(re.compile(re.escape(UIRoutes.COMPARISON)))
    expect(comparison_page.get_page_heading()).to_be_visible()

    # Verify the product name is displayed in the comparison table
    expect(comparison_page.get_product_name_in_table(product_name)).to_be_visible()

    # Verify the product image is displayed
    expect(comparison_page.get_product_image_in_table(product_name)).to_be_visible()

    # Verify the product price is displayed
    expect(comparison_page.get_product_price_in_table()).to_be_visible()

    # Verify the 'Add to Cart' button is displayed
    expect(comparison_page.get_add_to_cart_button_in_table()).to_be_visible()

    # Verify the 'Remove' link is displayed
    expect(comparison_page.get_remove_link_in_table()).to_be_visible()
