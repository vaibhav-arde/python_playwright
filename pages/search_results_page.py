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
        self.lnk_product_compare = page.locator("#compare-total")

    # ===== Page Header =====

    def get_search_results_page_header(self):
        """Returns the header element of the search results page."""
        return self.search_page_header

    # ===== Product Verification =====

    def is_product_exist(self, product_name: str):
        """Check whether a specific product is displayed in search results."""
        product = self.search_products.filter(
            has_text=re.compile(rf"^\s*{re.escape(product_name)}\s*$")
        ).first
        try:
            product.wait_for(state="attached", timeout=3000)
            return product
        except Exception:
            return None

    # ===== Product Selection =====

    def select_product(self, product_name: str) -> ProductPage | None:
        """Select a product from search results by name."""
        self.wait_for(self.search_products.first, state="visible")
        product = self.search_products.filter(
            has_text=re.compile(rf"^\s*{re.escape(product_name)}\s*$")
        ).first
        self.click(product)
        product_page = ProductPage(self.page)
        expect(product_page.lbl_product_name).to_be_visible(timeout=10000)
        return product_page

    # ===== Product Count =====

    def get_product_count(self):
        """Returns all product locators found in search results."""
        return self.search_products

    def click_list_view(self):
        """Click the List view button."""
        self.click(self.page.locator("#list-view"))

    def click_grid_view(self):
        """Click the Grid view button."""
        self.click(self.page.locator("#grid-view"))

    def hover_compare_button(self, product_name: str):
        """Hover over the compare button for a specific product."""
        product_container = self.page.locator(".product-layout").filter(
            has=self.page.locator(
                "h4 a", has_text=re.compile(rf"^\s*{re.escape(product_name)}\s*$")
            )
        )
        product_container.locator("button").filter(has=self.page.locator("i.fa-exchange")).hover()

    def get_compare_button_tooltip(self, product_name: str) -> str:
        """Return the tooltip text of the compare button for a specific product."""
        product_container = self.page.locator(".product-layout").filter(
            has=self.page.locator(
                "h4 a", has_text=re.compile(rf"^\s*{re.escape(product_name)}\s*$")
            )
        )
        button = product_container.locator("button").filter(has=self.page.locator("i.fa-exchange"))
        tooltip = self.get_element_attribute(button, "title")
        if not tooltip:
            tooltip = self.get_element_attribute(button, "data-original-title")
        return tooltip or ""

    def click_product_compare_link(self):
        """Click on the 'Product Compare' link."""
        self.click(self.lnk_product_compare)

    def click_product_comparison_link(self):
        """Alias for click_product_compare_link."""
        self.click_product_compare_link()

    def click_compare_button(self, product_name: str):
        """Click the compare button for a specific product in search results."""
        product_container = self.page.locator(".product-layout").filter(
            has=self.page.locator(
                "h4 a", has_text=re.compile(rf"^\s*{re.escape(product_name)}\s*$")
            )
        )
        self.click(
            product_container.locator("button").filter(has=self.page.locator("i.fa-exchange"))
        )

    def get_compare_success_message(self) -> str:
        """Return the text of the comparison success message."""
        success_alert = self.page.locator("div.alert-success")
        self.wait_for(success_alert, state="visible")
        return self.get_text(success_alert)
