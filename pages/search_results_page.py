# pages/search_results_page.py
# =====================
# Page Object for the Search Results Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.product_page import ProductPage


class SearchResultsPage(BasePage):
    """Page Object Model class for the Search Results Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.search_page_header = page.locator("#content").get_by_role("heading", level=1)
        self.search_products = page.locator("h4 > a")
        self.msg_empty_search = page.get_by_text(
            "There is no product that matches the search criteria."
        )
        self.txt_search_criteria = page.locator("#input-search")

    # ===== Page Header =====

    def get_search_results_page_header(self):
        """Returns the header element of the search results page."""
        return self.search_page_header

    def get_search_criteria_textbox(self):
        """Returns the search criteria text box locator on the search results page."""
        return self.txt_search_criteria

    def get_empty_search_message(self):
        """Returns the locator for the empty search results message."""
        return self.msg_empty_search

    # ===== Product Verification =====

    def is_product_exist(self, product_name: str):
        """Check whether a specific product is displayed in search results."""
        count = self.search_products.count()
        for i in range(count):
            product = self.search_products.nth(i)
            title = product.text_content()
            if title and title.strip() == product_name:
                return product
        return None

    # ===== Product Selection =====

    def select_product(self, product_name: str) -> ProductPage | None:
        """Select a product from search results by name."""
        count = self.search_products.count()
        for i in range(count):
            product = self.search_products.nth(i)
            title = product.text_content()
            if title and title.strip() == product_name:
                self.click(product)
                return ProductPage(self.page)
        return None

    # ===== Product Count =====

    def get_product_count(self):
        """Returns all product locators found in search results."""
        return self.search_products

    def get_products_by_search_term(self, search_term: str):
        """Returns a locator of products filtered by the given search term text."""
        return self.search_products.filter(has_text=search_term)
