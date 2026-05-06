import re
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.desktop_category_page import DesktopCategoryPage
from pages.product_comparison_page import ProductComparisonPage
from utils.constants import UIRoutes
from utils.messages import EMPTY_COMPARISON_MESSAGE


@pytest.mark.regression
@pytest.mark.ui
def test_validate_empty_product_compare_page(page):
    """
    Test Case: TC_PC_010
    Objective: Validate 'Product Compare' page when no products are added for comparison
    """
    home_page = HomePage(page)
    desktop_category_page = DesktopCategoryPage(page)
    comparison_page = ProductComparisonPage(page)

    # Step 1: Hover the mouse on any Menu say 'Desktops' and select 'Show All Desktops' option
    home_page.hover_desktops_menu()
    home_page.click_show_all_desktops()

    # Step 2: In the displayed 'Desktops' category page, click on 'Product Compare(0)' link
    # Verify ER-1: Category page is displayed
    expect(desktop_category_page.get_category_page_header()).to_be_visible()

    # Click on 'Product Compare' link
    desktop_category_page.click_product_compare_link()

    # Acceptance Criteria:
    # 1. User should be taken to 'Product Compare' page
    comparison_page.verify_url(re.compile(re.escape(UIRoutes.COMPARISON)))
    expect(comparison_page.get_page_heading()).to_be_visible()

    # 2. 'You have not chosen any products to compare.' should be displayed on the page
    actual_message = comparison_page.get_empty_comparison_message_text()
    assert actual_message == EMPTY_COMPARISON_MESSAGE
