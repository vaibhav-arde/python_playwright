import re
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.desktop_category_page import DesktopCategoryPage
from pages.product_comparison_page import ProductComparisonPage
from utils.constants import UIRoutes


@pytest.mark.regression
@pytest.mark.ui
def test_navigate_to_product_compare_page_from_category_page(page):
    """
    Test Case: TC_PC_009
    Objective: Validate navigating to 'Product Compare' page from Product Category page
    """
    home_page = HomePage(page)
    desktop_category_page = DesktopCategoryPage(page)
    comparison_page = ProductComparisonPage(page)

    # Step 1: Hover the mouse on any Menu say 'Desktops' and select 'Show All Desktops' option
    home_page.hover_desktops_menu()
    home_page.click_show_all_desktops()

    # Step 2: In the displayed 'Desktops' category page, click on 'Product Compare' link
    # ER-1: Desktops category page should be displayed
    expect(desktop_category_page.get_category_page_header()).to_be_visible()

    # Click on 'Product Compare' link
    desktop_category_page.click_product_compare_link()

    # Acceptance Criteria: User should be taken to 'Product Compare' page
    expect(page).to_have_url(re.compile(re.escape(UIRoutes.COMPARISON)))
    expect(comparison_page.get_page_heading()).to_be_visible()
