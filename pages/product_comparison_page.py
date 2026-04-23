# pages/product_comparison_page.py
# =====================
# Page Object for the Product Comparison Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page
from pages.base_page import BasePage


class ProductComparisonPage(BasePage):
    """Page Object Model class for the Product Comparison Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.lbl_heading = page.get_by_role("heading", name="Product Comparison")
        self.comparison_table = page.locator("table.table-bordered")

    # ===== Action Methods =====

    def is_product_in_comparison(self, product_name: str) -> bool:
        """Verify if the product name appears in the comparison table rows."""
        # Use a more robust check that looks specifically at the product names in the table
        product_link = self.comparison_table.get_by_role("link", name=product_name).first
        try:
            product_link.wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False
