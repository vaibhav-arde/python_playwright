import re

import pytest
from playwright.sync_api import expect

from pages.desktop_category_page import DesktopCategoryPage
from pages.home_page import HomePage
from pages.product_comparison_page import ProductComparisonPage
from utils.constants import UIRoutes
from utils.messages import COMPARE_BUTTON_TOOLTIP, COMPARE_SUCCESS


@pytest.mark.regression
@pytest.mark.ui
def test_add_product_from_desktops_category_list_view_for_comparison(page):
    """Verify that a product can be added to comparison from the Desktops category list view."""

    expected_tooltip = COMPARE_BUTTON_TOOLTIP

    home_page = HomePage(page)
    desktops_page = DesktopCategoryPage(page)

    # Step 1: Hover the Desktops menu and open the full category listing
    home_page.hover_desktops_menu()
    expect(home_page.get_show_all_desktops_link()).to_be_visible()
    home_page.click_show_all_desktops()

    # Step 2: Verify the Desktops category page is displayed
    expect(desktops_page.get_category_page_header()).to_be_visible()

    # Step 3: Switch to list view
    desktops_page.click_list_view()

    # Step 4: Use the first visible product on the page
    expect(desktops_page.get_first_product_card()).to_be_visible()
    product_name = desktops_page.get_first_product_name()

    # Hover the compare button for that product and validate the tooltip
    desktops_page.hover_compare_button(product_name)

    actual_tooltip = desktops_page.get_compare_button_tooltip(product_name)
    assert actual_tooltip == expected_tooltip

    # Step 5: Click 'Compare this Product'
    desktops_page.click_compare_button(product_name)

    # Step 6: Validate the success message
    expected_success_msg = COMPARE_SUCCESS.format(product_name=product_name)
    actual_success_msg = desktops_page.get_compare_success_message()

    assert expected_success_msg in actual_success_msg

    # Step 7: Open the comparison page
    desktops_page.click_product_comparison_link()

    comparison_page = ProductComparisonPage(page)

    # Step 8: Validate the Product Comparison page and product entry
    expect(page).to_have_url(re.compile(re.escape(UIRoutes.COMPARISON)))
    expect(comparison_page.get_page_heading()).to_be_visible()
    expect(comparison_page.get_product_name_in_table(product_name)).to_be_visible()
