# pages/product_page.py

# =====================

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
        self.cnf_msg = page.locator("div.alert.alert-success.alert-dismissible")
        self.lnk_shopping_cart_success_msg = self.cnf_msg.get_by_role("link", name="shopping cart")
        self.btn_items = page.locator("#cart")
        self.lnk_view_cart = page.locator('strong:has-text("View Cart")')

        # ===== Quantity Methods =====

    def set_quantity(self, qty: str):
        """Set the desired product quantity."""
        self.fill(self.txt_quantity, "")
        self.fill(self.txt_quantity, qty)

        # ===== Add to Cart Methods =====

    def add_to_cart(self):
        """Click the 'Add to Cart' button."""
        self.click(self.btn_add_to_cart)

    # ===== Confirmation Message =====
    def get_confirmation_message(self):
        """Return the confirmation message element."""
        return self.cnf_msg

    def click_shopping_cart_in_success_message(self) -> ShoppingCartPage:
        """Click the 'shopping cart' link within the success message."""
        self.cnf_msg.wait_for(state="visible")
        self.lnk_shopping_cart_success_msg.click()
        return ShoppingCartPage(self.page)

    # ===== Navigate to Shopping Cart =====
    def click_items_to_navigate_to_cart(self) -> ShoppingCartPage:
        self.click(self.btn_items)
        return ShoppingCartPage(self.page)

    def click_view_cart(self) -> ShoppingCartPage:
        self.click(self.lnk_view_cart)
        return ShoppingCartPage(self.page)

    # ===== Combined Workflow =====
    def add_product_to_cart(self, quantity: str):
        self.set_quantity(quantity)
        self.add_to_cart()
        expect(self.get_confirmation_message()).to_be_visible()
