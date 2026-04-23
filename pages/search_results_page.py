# pages/search_results_page.py
# =====================
# Page Object for the Search Results Page.
# Inherits from BasePage for reusable UI interaction methods.

import re
from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.product_page import ProductPage

class SearchResultsPage(BasePage):
    """Page Object Model class for the Search Results Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.search_page_header = page.get_by_role("heading", name=re.compile(r"^Search -"))
        self.search_products = page.locator("#content h4 > a")

    # ===== Page Header =====

    def get_search_results_page_header(self):
        """Returns the header element of the search results page."""
        return self.search_page_header

    # ===== Product Verification =====

    def is_product_exist(self, product_name: str):
        """Check whether a specific product is displayed in search results."""
        product = self.search_products.filter(has_text=re.compile(rf"^\s*{re.escape(product_name)}\s*$")).first
        try:
            product.wait_for(state="attached", timeout=3000)
            return product
        except Exception:
            return None

    # ===== Product Selection =====

    def select_product(self, product_name: str) -> ProductPage | None:
        """Select a product from search results by name."""
        product = self.search_products.filter(has_text=re.compile(rf"^\s*{re.escape(product_name)}\s*$")).first
        self.click(product)
        product_page = ProductPage(self.page)
        expect(product_page.lbl_product_name).to_be_visible(timeout=10000)
        return product_page

    # ===== Product Count =====

    def get_product_count(self):
        """Returns all product locators found in search results."""
        return self.search_products
