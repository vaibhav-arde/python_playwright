# pages/product_comparison_page.py
# =====================
# Page Object for the Product Comparison Page.
# Inherits from BasePage for reusable UI interaction methods.

import re

from playwright.sync_api import Page

from pages.base_page import BasePage
from utils import messages


class ProductComparisonPage(BasePage):
    """Page Object Model class for the Product Comparison page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        # Heading: role="heading" scoped to the page content area
        self.page_heading = page.get_by_role("heading", name="Product Comparison", exact=True)
        self.empty_comparison_text = page.locator("#content").get_by_text(
            messages.EMPTY_COMPARISON_MESSAGE
        )
        self.btn_continue = page.get_by_role("link", name="Continue")

    # ===== Page Header =====

    def get_page_heading(self):
        """Return the 'Product Comparison' heading locator."""
        return self.page_heading

    def get_empty_comparison_message_text(self) -> str:
        """Return the text displayed when no products are added for comparison."""
        return self.get_text(self.empty_comparison_text)

    # ===== Continue Button =====

    def get_continue_button(self):
        """Return the 'Continue' button locator."""
        return self.btn_continue

    def click_continue(self):
        """Click the 'Continue' button to navigate back to the Home page."""
        self.click(self.btn_continue)

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
