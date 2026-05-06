import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.product_comparison_page import ProductComparisonPage
from utils.constants import UIRoutes
from utils.messages import COMPARE_BUTTON_TOOLTIP, COMPARE_SUCCESS


@pytest.mark.regression
@pytest.mark.ui
def test_add_product_from_featured_section_home_page_for_comparison(page):
    """Verify that a product can be added to comparison from the Featured section on the Home Page."""

    home_page = HomePage(page)

    # Step 1: Hover 'Compare this Product' from the Featured section of Home Page
    # First, get the name of the featured product to validate later
    featured_product_name = home_page.get_first_featured_product_name()

    home_page.hover_featured_compare_button()

    # Validate ER-1: Tooltip with the text - 'Compare this Product' should be displayed
    actual_tooltip = home_page.get_featured_compare_button_tooltip()
    assert actual_tooltip == COMPARE_BUTTON_TOOLTIP

    # Step 2: Select 'Compare this Product'
    home_page.click_featured_compare_button()

    # Validate ER-2: Success message with text - ' Success: You have added Product Name to your product comparison!'
    expected_success_msg = COMPARE_SUCCESS.format(product_name=featured_product_name)
    actual_success_msg = home_page.get_compare_success_message()
    assert expected_success_msg in actual_success_msg

    # Step 3: Click on 'product comparison' link from the displayed success message
    home_page.click_product_comparison_link()

    # Validate ER-3: User should be taken to the 'Product Comparison' page with the details of the product
    comparison_page = ProductComparisonPage(page)

    expect(page).to_have_url(re.compile(re.escape(UIRoutes.COMPARISON)))
    expect(comparison_page.get_page_heading()).to_be_visible()
    expect(comparison_page.get_product_name_in_table(featured_product_name)).to_be_visible()
