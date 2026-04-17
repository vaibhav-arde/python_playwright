<<<<<<< HEAD
# pages/search_results_page.py
# =====================
# Page Object for the Search Results Page.
# Inherits from BasePage for reusable UI interaction methods.

import re

from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.product_page import ProductPage


class SearchResultsPage(BasePage):
    """Page Object Model class for the Search Results Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.search_page_header = page.get_by_role("heading", name=re.compile(r"^Search -"))
        self.grid_view_button = page.get_by_role("button").filter(has=page.locator(".fa-th")).first
        self.list_view_button = (
            page.get_by_role("button").filter(has=page.locator(".fa-th-list")).first
        )
        self.compare_success_message = page.locator("div.alert.alert-success.alert-dismissible")
        self.lnk_product_comparison = self.compare_success_message.get_by_role(
            "link", name="product comparison"
        )
        self.product_links = page.locator(".product-layout").get_by_role("link")
        self.lnk_product_compare = page.get_by_role("link", name=re.compile(r"Product Compare"))

    # ===== Page Header =====

    def get_search_results_page_header(self):
        """Returns the header element of the search results page."""
        return self.search_page_header

    # ===== View Selection =====

    def click_list_view(self):
        """Switch the search results to list view."""
        self.click(self.list_view_button)

    def click_grid_view(self):
        """Switch the search results to grid view."""
        self.click(self.grid_view_button)

    # ===== Product Verification =====

    def get_product_link(self, product_name: str):
        """Return the product title link inside the product card."""
        return (
            self.page.locator(".product-layout")
            .filter(has_text=product_name)
            .get_by_role("link", name=product_name)
            .first
        )

    def is_product_exist(self, product_name: str):
        """Check whether a specific product is displayed in search results."""
        return self.get_product_link(product_name)

    # ===== Product Selection =====

    def select_product(self, product_name: str) -> ProductPage | None:
        """Select a product from search results by name."""
        product = self.get_product_link(product_name)
        try:
            self.wait_for(product, state="visible")
        except Exception:
            return None
        self.click(product)
        return ProductPage(self.page)

    # ===== Product Comparison in List View =====

    def get_compare_button(self, product_name: str):
        """Return the 'Compare this Product' button for a specific product."""
        return (
            self.page.locator(".product-layout")
            .filter(has_text=product_name)
            .get_by_role("button")
            .filter(has=self.page.locator(".fa-exchange"))
            .first
        )

    def get_compare_button_tooltip(self, product_name: str) -> str | None:
        """Return the tooltip text for the list-view compare button."""
        return self.get_attribute(self.get_compare_button(product_name), "data-original-title")

    def hover_compare_button(self, product_name: str):
        """Hover over the list-view compare button for a specific product."""
        self.hover(self.get_compare_button(product_name))

    def click_compare_button(self, product_name: str):
        """Click the list-view compare button for a specific product."""
        self.click(self.get_compare_button(product_name))

    def get_compare_success_message(self) -> str:
        """Return the comparison success message shown after adding a product."""
        self.wait_for(self.compare_success_message, state="visible")
        return self.get_text(self.compare_success_message)

    def click_product_comparison_link(self):
        """Click the 'product comparison' link from the success message."""
        self.click(self.lnk_product_comparison)

    def click_product_compare_link(self):
        """Click the 'Product Compare' link displayed above the search results."""
        self.click(self.lnk_product_compare)

    # ===== Product Count =====

    def get_product_count(self):
        """Returns product link locators found in search results."""
        return self.product_links
=======
# pages/search_results_page.py

from playwright.sync_api import Page
from pages.base_page import BasePage


class SearchResultsPage(BasePage):
    """Page Object Model class for the Search Results Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        self.search_page_header = page.locator("#content h1", has_text="Search -")
        self.search_products = page.locator("h4 > a")

    def get_search_results_page_header(self):
        return self.search_page_header

    def is_product_exist(self, product_name: str):
        count = self.search_products.count()
        for i in range(count):
            product = self.search_products.nth(i)
            title = product.text_content()
            if title and title.strip() == product_name:
                return product
        return None

    def select_product(self, product_name: str):
        count = self.search_products.count()
        for i in range(count):
            product = self.search_products.nth(i)
            title = product.text_content()
            if title and title.strip() == product_name:
                self.click(product)

                # ✅ FIX: local import (avoids circular issue)
                from pages.product_page import ProductPage

                return ProductPage(self.page)

        return None

    def get_product_count(self):
        return self.search_products
>>>>>>> 6eddf17 (add testcases)
