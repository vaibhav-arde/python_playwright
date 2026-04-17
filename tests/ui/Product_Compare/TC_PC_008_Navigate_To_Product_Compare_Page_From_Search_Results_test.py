import re
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_comparison_page import ProductComparisonPage
from utils.constants import UIRoutes

from utils.data_loader import read_json_data


@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.datadriven
@pytest.mark.parametrize(("product_name",), read_json_data("test_data/comparedata.json"))
def test_navigate_to_product_compare_page_from_search_results(page, product_name):
    """
    Test Case: TC_PC_008
    Objective: Verify that user can navigate to 'Product Compare' page from Search Results page.
    """
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    comparison_page = ProductComparisonPage(page)

    # Step 1: Enter any existing Product name into the Search text box field
    home_page.enter_product_name(product_name)

    # Step 2: Click on the button having search icon
    home_page.click_search()

    # Step 3: Click on 'Product Compare' link displayed in the Search Results page
    expect(search_results_page.get_search_results_page_header()).to_be_visible()
    search_results_page.click_product_compare_link()

    # Acceptance Criteria: User should be taken to 'Product Compare' page
    expect(page).to_have_url(re.compile(re.escape(UIRoutes.COMPARISON)))
    expect(comparison_page.get_page_heading()).to_be_visible()
