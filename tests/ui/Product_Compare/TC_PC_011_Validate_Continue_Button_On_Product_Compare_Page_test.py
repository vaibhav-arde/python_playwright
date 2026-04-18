import re
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.desktop_category_page import DesktopCategoryPage
from pages.product_comparison_page import ProductComparisonPage
from utils.constants import UIRoutes


@pytest.mark.regression
@pytest.mark.ui
def test_validate_continue_button_on_product_compare_page(page):
    home_page = HomePage(page)
    desktop_category_page = DesktopCategoryPage(page)
    comparison_page = ProductComparisonPage(page)

    # Step 1: Hover the mouse on any Menu say 'Desktops' and select 'Show All Desktops' option
    home_page.hover_desktops_menu()
    home_page.click_show_all_desktops()

    # Step 2: In the displayed 'Desktops' category page, click on 'Product Compare(0)' link
    expect(desktop_category_page.get_category_page_header()).to_be_visible()
    desktop_category_page.click_product_compare_link()

    # Verify the Product Comparison page is displayed
    comparison_page.verify_url(re.compile(re.escape(UIRoutes.COMPARISON)))
    expect(comparison_page.get_page_heading()).to_be_visible()

    # Step 3: Click on the 'Continue' button
    expect(comparison_page.get_continue_button()).to_be_visible()
    comparison_page.click_continue()

    # Acceptance Criteria: User should be navigated to 'Home' page
    comparison_page.verify_url(re.compile(re.escape(UIRoutes.HOME)))
