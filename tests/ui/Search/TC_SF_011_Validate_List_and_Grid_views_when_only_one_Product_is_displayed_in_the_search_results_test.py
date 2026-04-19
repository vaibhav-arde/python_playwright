"""
Test Case ID: #49
Description: Validate List and Grid views when only one Product is displayed in the search results

1. Enter any existing product name into the 'Search' text box field -
2. Click on the button having search icon
3. Select 'List' option (Validate ER-1)
4. Click on the Image of the Product and name of the product (Validate ER-2)
5. Repeat Steps 1 to 2 and Select 'Grid' option (Validate ER-3)
6. Click on the Image of the Product and name of the product (Validate ER-4)

"""

import pytest
import re
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.config import Config
from utils.constants import UIRoutes


@pytest.mark.ui
def test_list_and_grid_view_with_single_product(page):
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    product_name = Config.product_name

    # Search product
    home_page.enter_product_name(product_name)
    home_page.click_search()

    expect(search_results_page.get_search_results_page_header()).to_be_visible()

    # -------- LIST VIEW --------
    search_results_page.click_list_view()

    # ER-1: Single product should be displayed
    expect(search_results_page.get_product_count()).to_have_count(1)
    expect(search_results_page.get_product_container(product_name)).to_be_visible()

    # Validate actions (Add to Cart, Wish List and Compare Product) are working
    search_results_page.click_add_to_cart(product_name)
    expect(search_results_page.get_success_message(product_name)).to_be_visible()

    search_results_page.click_wishlist(product_name)
    expect(search_results_page.get_success_message(product_name)).to_be_visible()

    search_results_page.click_compare(product_name)
    expect(search_results_page.get_success_message(product_name)).to_be_visible()

    # Navigate via image (ER-2)
    search_results_page.click_product_image(product_name)
    expect(page).to_have_url(re.compile(UIRoutes.PRODUCT_PAGE))
    page.go_back()
    expect(search_results_page.get_search_results_page_header()).to_be_visible()

    # -------- GRID VIEW --------
    search_results_page.click_grid_view()

    # ER-3: Single product should be displayed
    expect(search_results_page.get_product_count()).to_have_count(1)
    expect(search_results_page.get_product_container(product_name)).to_be_visible()

    # Validate actions
    search_results_page.click_add_to_cart(product_name)
    expect(search_results_page.get_success_message(product_name)).to_be_visible()

    search_results_page.click_wishlist(product_name)
    expect(search_results_page.get_success_message(product_name)).to_be_visible()

    search_results_page.click_compare(product_name)
    expect(search_results_page.get_success_message(product_name)).to_be_visible()

    # Navigate via product name (ER-4)
    search_results_page.click_product_link(product_name)
    expect(page).to_have_url(re.compile(UIRoutes.PRODUCT_PAGE))
