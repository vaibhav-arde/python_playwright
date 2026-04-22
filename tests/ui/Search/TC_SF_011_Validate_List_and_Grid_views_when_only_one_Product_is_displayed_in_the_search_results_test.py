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
from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.config import Config
from utils.assertions import assert_single_product


@pytest.mark.ui
def test_list_and_grid_view_with_single_product(page):
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)

    product_name = Config.product_name

    # Search product
    home_page.enter_product_name(product_name)
    home_page.click_search()

    expect(search_results_page.get_search_results_page_header()).to_be_visible()

    # -------- LIST VIEW --------
    search_results_page.click_list_view()

    products = search_results_page.get_product_count()
    assert_single_product(products)

    search_results_page.perform_basic_product_actions(product_name)
    search_results_page.assert_success_message_visible(product_name)

    search_results_page.open_product_via_image(product_name)
    product_page.assert_product_page_opened()
    page.go_back()

    # -------- GRID VIEW --------
    search_results_page.click_grid_view()

    products = search_results_page.get_product_count()
    assert_single_product(products)

    search_results_page.perform_basic_product_actions(product_name)
    search_results_page.assert_success_message_visible(product_name)

    search_results_page.open_product_via_link(product_name)
    product_page.assert_product_page_opened()
