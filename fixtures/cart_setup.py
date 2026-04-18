# fixtures/cart_setup.py
# =====================
# Fixtures for cart-related preconditions.

import pytest
from api_clients.cart_api import CartAPI
from utils.config import Config


@pytest.fixture
def cart_with_products(api_context, authenticated_session):
    """
    Ensures the user has specific products in their cart via API.
    """
    cart_api = CartAPI(api_context)

    # Add target product (ID would typically come from a product catalog API or Config)
    # Here we use a placeholder ID "123" as a representative example
    cart_api.add_item_to_cart(product_id="123", quantity=int(Config.product_quantity))

    return True
