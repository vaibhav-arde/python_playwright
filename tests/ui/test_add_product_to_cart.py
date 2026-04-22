"""
TC_CART_001
(TS_001) Add Product to Cart

Validate user can add product to the Shopping Cart

1. Search for a product by name
2. Select the product from results
3. Set quantity and click Add to Cart
4. Verify success confirmation message
"""

import pytest

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.config import Config


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.xfail
def test_add_product_to_cart(page):
    """Verify user can search and add a product to the cart."""

    product_name = Config.product_name
    quantity = Config.product_quantity

    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    # Step 1: Search for product
    home_page.enter_product_name(product_name)
    home_page.click_search()

    # Step 2: Select product
    product_page = search_results_page.select_product(product_name)

    # Step 3: Set quantity and add to cart
    product_page.set_quantity(quantity)
    product_page.add_to_cart()

    # Step 4: Verify confirmation message
    product_page.verify_product_added_successfully()
