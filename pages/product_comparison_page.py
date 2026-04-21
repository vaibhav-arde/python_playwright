# pages/product_comparison_page.py
# =====================
# Page Object for the Product Comparison Page.
# Inherits from BasePage for reusable UI interaction methods.

import re
from playwright.sync_api import Page
from pages.base_page import BasePage

class ProductComparisonPage(BasePage):
    """Page Object Model class for the Product Comparison Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.lbl_heading = page.locator("#content h1")
        self.comparison_table = page.locator("div.table-responsive")

    # ===== Action Methods =====

    def is_product_in_comparison(self, product_name: str) -> bool:
        """Verify if the product name appears in the comparison table."""
        try:
            self.comparison_table.get_by_text(product_name).first.wait_for(state="visible", timeout=10000)
            return True
        except Exception:
            return False
