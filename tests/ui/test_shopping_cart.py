# tests/ui/test_shopping_cart.py
# ==================================
# Validates shopping cart totals and contents using API-driven setup.

from playwright.sync_api import expect
from pages.product_page import ProductPage
from utils.config import Config


def test_shopping_cart_validation_ui(page, authenticated_session, cart_with_products):
    """Verify the cart total price matches the expected configuration."""
    product_page = ProductPage(page)

    # Navigate directly to cart
    product_page.click_items_to_navigate_to_cart()
    shopping_cart = product_page.click_view_cart()

    expect(shopping_cart.get_total_price()).to_have_text(Config.total_price)
