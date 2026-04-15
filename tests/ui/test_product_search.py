# tests/ui/test_product_search.py
# ==================================
# Validates product search and selection UI.

from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.config import Config


def test_product_search_ui(page, authenticated_session):
    """Verify that a user can search for and select a product."""
    product_name = Config.product_name
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    home_page.enter_product_name(product_name)
    home_page.click_search()

    expect(search_results_page.get_search_results_page_header()).to_be_visible(timeout=5000)
    expect(search_results_page.is_product_exist(product_name)).to_be_visible(timeout=5000)

    product_page = search_results_page.select_product(product_name)
    expect(product_page).to_be_visible()
