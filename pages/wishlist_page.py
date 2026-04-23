# pages/wishlist_page.py
# =====================
# Page Object for the Wishlist Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page, Locator

from pages.base_page import BasePage


class WishlistPage(BasePage):
    """Page Object Model class for the Wishlist Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.wishlist_table = page.locator("table.table-bordered.table-hover")
        self.wishlist_rows = self.wishlist_table.locator("tbody tr")

    # ===== Wishlist Interactions =====

    def is_product_in_wishlist(self, product_name: str) -> Locator:
        """Check if a specific product is displayed in the wishlist and return its locator."""
        return self.wishlist_table.get_by_role("cell", name=product_name).first
