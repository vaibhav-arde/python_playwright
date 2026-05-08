# pages/wishlist_page.py
# =====================
# Page Object for the Wish List Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.product_page import ProductPage
from utils.constants import UILabels


class WishListPage(BasePage):
    """Page Object Model class for the Wish List Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.lbl_heading = page.get_by_role("heading", name=UILabels.WISHLIST_PAGE_HEADING)
        self.product_items = page.locator("div.table-responsive table tbody tr")
        self.lnk_product_image = self.product_items.locator("td.text-center a, td.image a")
        self.lnk_product_name = self.product_items.locator("td.name a, td.text-left a")
        self.btn_remove = self.product_items.get_by_role("link", name="Remove")
        self.btn_add_to_cart = self.product_items.locator("button[title*='Add to Cart' i], button[data-original-title*='Add to Cart' i]")
        self.cnf_msg = page.locator("div.alert.alert-success, div.alert-success")

    # ===== Action Methods =====

    def get_page_heading(self):
        """Return the page heading locator."""
        return self.lbl_heading

    def get_product_row_by_name(self, product_name: str):
        """Find the row containing the specified product name."""
        return self.product_items.filter(
            has=self.page.get_by_role("link", name=product_name, exact=True)
        ).first

    def click_add_to_cart(self, product_name: str):
        """Click the Add to Cart button for the specified product."""
        row = self.get_product_row_by_name(product_name)
        self.click(row.locator("button[title*='Add to Cart' i], button[data-original-title*='Add to Cart' i]").first)

    def get_confirmation_message(self):
        """Return the confirmation message element shown after adding to cart."""
        return self.cnf_msg

    def click_product_image(self, product_name: str) -> ProductPage:
        """Click the image of the specified product in the Wish List."""
        row = self.get_product_row_by_name(product_name)
        self.click(row.locator("td.text-center a, td.image a").first)
        return ProductPage(self.page)

    def click_product_name(self, product_name: str) -> ProductPage:
        """Click the name link of the specified product in the Wish List."""
        row = self.get_product_row_by_name(product_name)
        self.click(row.locator("td.text-left a, td.name a").first)
        return ProductPage(self.page)
