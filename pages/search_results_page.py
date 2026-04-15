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
        self.list_view_button = page.locator("#list-view")
        self.compare_success_message = page.locator("div.alert.alert-success.alert-dismissible")
        self.lnk_product_comparison = self.compare_success_message.get_by_role(
            "link", name="product comparison"
        )
        self.product_links = page.locator(".product-layout h4 > a")

    # ===== Page Header =====

    def get_search_results_page_header(self):
        """Returns the header element of the search results page."""
        return self.search_page_header

    # ===== View Selection =====

    def click_list_view(self):
        """Switch the search results to list view."""
        self.click(self.list_view_button)

    # ===== Product Verification =====

    # def get_product_link(self, product_name: str):
    #     """Return the product link for a specific search result."""
    #     return self.page.get_by_role("link", name=product_name, exact=True)

    def get_product_link(self, product_name: str):
        """Return the product title link inside the product card."""
        return self.get_product_card(product_name).locator("h4 a")

    def is_product_exist(self, product_name: str):
        """Check whether a specific product is displayed in search results."""
        return self.get_product_link(product_name)

    # ===== Product Selection =====

    def select_product(self, product_name: str) -> ProductPage | None:
        """Select a product from search results by name."""
        product = self.get_product_link(product_name)
        if product.count() == 0:
            return None
        self.click(product)
        return ProductPage(self.page)

    # ===== Product Comparison in List View =====

    def get_product_card(self, product_name: str):
        """Return the product card locator for a product in list view."""
        return self.page.locator(".product-layout").filter(has_text=product_name).first

    def get_compare_button(self, product_name: str):
        """Return the 'Compare this Product' button for a specific product."""
        return self.get_product_card(product_name).locator(
            'button[data-original-title="Compare this Product"]'
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

    # ===== Product Count =====

    def get_product_count(self):
        """Returns product link locators found in search results."""
        return self.product_links
