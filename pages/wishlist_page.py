# pages/wishlist_page.py
# =====================
# Page Object for the Wish List Page.
# Inherits from BasePage for reusable UI interaction methods.

import re
from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.product_page import ProductPage

class WishListPage(BasePage):
    """Page Object Model class for the Wish List Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.lbl_heading = page.locator("#content h2, #content h1").filter(has_text=re.compile(r"Wish List", re.IGNORECASE))
        self.product_items = page.locator(".table tr")
        self.lnk_product_image = self.product_items.locator("td.image a")
        self.lnk_product_name = self.product_items.locator("td.name a")
        self.btn_remove = self.product_items.locator("td.button a")

    # ===== Action Methods =====

    def get_product_row_by_name(self, product_name: str):
        """Find the row containing the specified product name."""
        return self.product_items.filter(has_text=product_name).first

    def click_product_image(self, product_name: str) -> ProductPage:
        """Click the image of the specified product in the Wish List."""
        row = self.get_product_row_by_name(product_name)
        self.click(row.locator("td.image a"))
        return ProductPage(self.page)

    def click_product_name(self, product_name: str) -> ProductPage:
        """Click the name link of the specified product in the Wish List."""
        row = self.get_product_row_by_name(product_name)
        self.click(row.locator("td.name a"))
        return ProductPage(self.page)
