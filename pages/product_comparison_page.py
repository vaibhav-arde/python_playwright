# pages/product_comparison_page.py
# =====================
# Page Object for the Product Comparison Page.
# Inherits from BasePage for reusable UI interaction methods.

import re

from playwright.sync_api import Page

from pages.base_page import BasePage


class ProductComparisonPage(BasePage):
    """Page Object Model class for the Product Comparison page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        # Heading: role="heading" scoped to the page content area
        self.page_heading = page.get_by_role("heading", name="Product Comparison", exact=True)

    # ===== Page Header =====

    def get_page_heading(self):
        """Return the 'Product Comparison' heading locator."""
        return self.page_heading

    # ===== Product Presence in Table =====

    def get_product_name_in_table(self, product_name: str):
        """Return the locator for the exact product name cell in the comparison table.

        Uses get_by_role('cell') and filters with an exact-match regex
        to avoid strict-mode violations from description cells that also
        contain the product name.
        """
        return self.page.get_by_role("cell").filter(
            has_text=re.compile(rf"^{re.escape(product_name)}$")
        )
