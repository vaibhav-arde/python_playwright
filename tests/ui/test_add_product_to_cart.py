"""
Test Case: Add Product to Cart

===========================================
Test Steps
===========================================
1. Search for a product by name.
2. Select the product from results.
3. Set quantity and click Add to Cart.
4. Verify success confirmation message.
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.config import Config


@pytest.mark.xfail
@pytest.mark.regression
def test_add_product_to_cart(page):
    """Verify user can search and add a product to the cart."""

    product_name = Config.product_name
    quantity = Config.product_quantity

    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    # Search for a product
    home_page.enter_product_name(product_name)
    home_page.click_search()

    # Select the product
    product_page = search_results_page.select_product(product_name)

    # Set quantity and add to cart
    product_page.set_quantity(quantity)
    product_page.add_to_cart()

    # Verify confirmation message
    expect(product_page.get_confirmation_message()).to_be_visible(timeout=10000)
