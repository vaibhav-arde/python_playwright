# api_clients/cart_api.py
# =====================
# API Client for shopping cart operations.

from playwright.sync_api import APIResponse
from api_clients.base_api import BaseAPI
from utils.constants import APIEndpoints


class CartAPI(BaseAPI):
    """API client for Cart management operations."""

    def add_item_to_cart(self, product_id: str, quantity: int) -> APIResponse:
        """
        Adds a specific product to the cart via API.

        :param product_id: The ID of the product to add
        :param quantity: Number of items to add
        :return: APIResponse object
        """
        payload = {"product_id": product_id, "quantity": quantity}
        return self.post(APIEndpoints.CART, data=payload)

    def clear_cart(self) -> APIResponse:
        """
        Clears all items from the current session's cart.

        :return: APIResponse object
        """
        return self.delete(APIEndpoints.CART)
