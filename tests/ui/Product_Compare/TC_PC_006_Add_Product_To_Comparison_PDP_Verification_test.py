import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.product_comparison_page import ProductComparisonPage
from pages.search_results_page import SearchResultsPage
from utils.constants import UIRoutes
from utils.data_loader import read_json_data
from utils.messages import COMPARE_BUTTON_TOOLTIP, COMPARE_SUCCESS


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize(("product_name",), read_json_data("test_data/comparedata.json"))
def test_add_product_to_comparison_pdp_verification(page, product_name):
    """Verify that a product can be added to comparison from the product display page."""

    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    # Step 1 & 2: Search for the existing product
    home_page.enter_product_name(product_name)
    home_page.click_search()

    expect(search_results_page.get_search_results_page_header()).to_be_visible()

    # Step 3: Open the product display page
    product_page = search_results_page.select_product(product_name)
    assert product_page is not None

    expect(product_page.get_product_header()).to_have_text(product_name)

    # Step 4: Hover 'Compare this Product' from the Related Products section
    # First, get the name of the related product to validate later
    related_product_name = product_page.get_related_product_name()

    product_page.hover_related_compare_button()

    actual_tooltip = product_page.get_related_compare_button_tooltip()
    assert actual_tooltip == COMPARE_BUTTON_TOOLTIP

    # Step 5: Select 'Compare this Product'
    product_page.click_related_compare_button()

    # Step 6: Validate the success message
    # The success message should contain the name of the related product
    expected_success_msg = COMPARE_SUCCESS.format(product_name=related_product_name)
    actual_success_msg = product_page.get_compare_success_message()
    assert expected_success_msg in actual_success_msg

    # Step 7: Open the Product Comparison page
    product_page.click_product_comparison_link()

    comparison_page = ProductComparisonPage(page)

    expect(page).to_have_url(re.compile(re.escape(UIRoutes.COMPARISON)))
    expect(comparison_page.get_page_heading()).to_be_visible()
    expect(comparison_page.get_product_name_in_table(related_product_name)).to_be_visible()
