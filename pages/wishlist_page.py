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
        self.btn_remove = self.product_items.locator("td.text-right a.btn-danger")

    # ===== Action Methods =====

    def get_page_heading(self):
        """Return the page heading locator."""
        return self.lbl_heading

    def get_product_row_by_name(self, product_name: str):
        """Find the row containing the specified product name."""
        return self.product_items.filter(has_text=product_name).filter(visible=True).first

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
