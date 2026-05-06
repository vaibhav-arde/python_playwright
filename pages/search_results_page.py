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
