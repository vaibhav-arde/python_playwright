# pages/category_page.py
# =====================
# Page Object for Category and Sub-category pages.
# Inherits from BasePage for reusable UI interaction methods.

import re
from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.shopping_cart_page import ShoppingCartPage

class CategoryPage(BasePage):
    """Page Object Model class for Category and Sub-category pages."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.lbl_category_name = page.get_by_role("heading", level=1)
        self.list_subcategory = page.locator("div.list-group a")
        self.product_thumbs = page.locator(".product-thumb")
        self.cnf_msg = page.locator("div.alert.alert-success, div.alert-success")
        self.lnk_shopping_cart_success = self.cnf_msg.get_by_role("link", name="shopping cart")

    # ===== Sub-category Methods =====

    def select_subcategory(self, subcategory_name: str):
        """Select a subcategory from the left side list group."""
        # Relaxed regex to match even if there are prefixes like " - " or counts like " (1)"
        self.list_subcategory.filter(has_text=re.compile(rf"{re.escape(subcategory_name)}", re.IGNORECASE)).click()

    # ===== Product Methods =====

    def click_add_to_cart(self, product_name: str):
        """Click 'Add to Cart' for a specific product in the category page."""
        product_thumb = self.product_thumbs.filter(
            has=self.page.get_by_role("link", name=product_name, exact=True)
        )
        # Using a regex to find the button with "Add to Cart" text
        self.click(product_thumb.get_by_role("button", name=re.compile(r"Add to Cart", re.IGNORECASE)))

    # ===== Confirmation Message Methods =====

    def get_confirmation_message(self):
        """Return the confirmation message locator."""
        return self.cnf_msg

    def click_shopping_cart_link(self) -> ShoppingCartPage:
        """Click the 'shopping cart' link from the success message."""
        self.click(self.lnk_shopping_cart_success)
        return ShoppingCartPage(self.page)
