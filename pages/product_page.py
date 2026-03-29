# pages/product_page.py
# =====================
# Page Object for the Product Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.shopping_cart_page import ShoppingCartPage


class ProductPage(BasePage):
    """Page Object Model class for the Product Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.txt_quantity = page.locator('input[name="quantity"]')
        self.btn_add_to_cart = page.locator("#button-cart")
        self.cnf_msg = page.locator("div.alert.alert-success")
        self.btn_items = page.locator("#cart")
        self.lnk_view_cart = page.locator('strong:has-text("View Cart")')

    # ===== Quantity Methods =====

    def set_quantity(self, qty: str):
        """Set the desired product quantity."""
        self.txt_quantity.fill("")
        self.txt_quantity.fill(qty)

    # ===== Add to Cart Methods =====

    def add_to_cart(self):
        """Click the 'Add to Cart' button."""
        # Wait for OpenCart's common.js event listener to attach to the button
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(500)
        self.btn_add_to_cart.click()

    # ===== Confirmation Message =====

    def get_confirmation_message(self):
        """Return the confirmation message element shown after adding to cart."""
        return self.cnf_msg

    # ===== Navigate to Shopping Cart =====

    def click_items_to_navigate_to_cart(self):
        """Click the cart icon to open the cart dropdown."""
        self.btn_items.click()

    def click_view_cart(self) -> ShoppingCartPage:
        """Click 'View Cart' link and return ShoppingCartPage instance."""
        self.lnk_view_cart.click()
        return ShoppingCartPage(self.page)

    # ===== Combined Workflow =====

    def add_product_to_cart(self, quantity: str):
        """Set quantity, add to cart, and verify confirmation message."""
        self.set_quantity(quantity)
        self.add_to_cart()
        expect(self.get_confirmation_message()).to_be_visible()
