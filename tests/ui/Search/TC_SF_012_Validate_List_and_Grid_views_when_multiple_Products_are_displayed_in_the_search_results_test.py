"""
Test Case ID: #50
Description: Validate List and Grid views when multiple Products are displayed in the search results

Steps:

1. Enter the search criteria in the 'Search' text box field which can result in multiple products -
2. Click on the button having search icon (Validate ER-1)
3. Select 'List' option (Validate ER-2)
4. Select 'Grid' option (Validate ER-3)

"""

import pytest
import re
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.config import Config
from utils.assertions import assert_products_match_search
from utils.constants import UIRoutes


@pytest.mark.ui
def test_list_and_grid_view_with_multiple_products(page):
    # Initialize page objects
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    search_term = Config.multiple_products_search_term

    # Step 1: Perform search with a term that returns multiple products
    home_page.enter_product_name(search_term)
    home_page.click_search()

    # Validate search results page is loaded
    expect(search_results_page.get_search_results_page_header()).to_be_visible()

    # Get all products from results
    products = search_results_page.get_product_count()

    # ER-1: Ensure more than one product is displayed
    assert products.count() > 1

    # Get first product name dynamically
    first_product = products.first.text_content().strip()

    # -------- LIST VIEW --------
    search_results_page.click_list_view()
    assert_products_match_search(products, search_term)

    # Validate Add to Cart
    search_results_page.click_add_to_cart(first_product)
    expect(search_results_page.get_success_message(first_product)).to_be_visible()

    # Validate Wishlist
    search_results_page.click_wishlist(first_product)
    expect(search_results_page.get_success_message(first_product)).to_be_visible()

    # Validate Compare
    search_results_page.click_compare(first_product)
    expect(search_results_page.get_success_message(first_product)).to_be_visible()

    # Validate navigation via image (List view)
    search_results_page.click_product_image(first_product)
    expect(page).to_have_url(re.compile(UIRoutes.PRODUCT_PAGE))

    page.go_back()

    # Validate navigation via product name (List view)
    search_results_page.click_product_link(first_product)
    expect(page).to_have_url(re.compile(UIRoutes.PRODUCT_PAGE))

    page.go_back()

    # -------- GRID VIEW --------
    search_results_page.click_grid_view()
    assert_products_match_search(products, search_term)

    # Validate Add to Cart (Grid view)
    search_results_page.click_add_to_cart(first_product)
    expect(search_results_page.get_success_message(first_product)).to_be_visible()

    # Validate Wishlist (Grid view)
    search_results_page.click_wishlist(first_product)
    expect(search_results_page.get_success_message(first_product)).to_be_visible()

    # Validate Compare (Grid view)
    search_results_page.click_compare(first_product)
    expect(search_results_page.get_success_message(first_product)).to_be_visible()

    # Validate navigation via image (Grid view)
    search_results_page.click_product_image(first_product)
    expect(page).to_have_url(re.compile(UIRoutes.PRODUCT_PAGE))

    page.go_back()

    # Validate navigation via product name (Grid view)
    search_results_page.click_product_link(first_product)
    expect(page).to_have_url(re.compile(UIRoutes.PRODUCT_PAGE))
