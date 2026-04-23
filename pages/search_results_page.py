# pages/search_results_page.py
# =====================
# Page Object for the Search Results Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.product_page import ProductPage
from pages.wishlist_page import WishlistPage
from utils.constants import ButtonNames


class SearchResultsPage(BasePage):
    """Page Object Model class for the Search Results Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.search_page_header = page.locator("#content h1", has_text="Search -")
        self.search_products = page.locator("h4 > a")
        self.success_msg = page.locator(".alert-success")
        self.lnk_wishlist_success = self.success_msg.get_by_role("link", name="wish list")

    # ===== Page Header =====

    def get_search_results_page_header(self):
        """Returns the header element of the search results page."""
        return self.search_page_header

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

    def add_product_to_wishlist(self, product_name: str):
        """Click 'Add to Wish List' for a specific product in search results."""
        product_container = self.page.locator(".product-layout").filter(
            has=self.page.get_by_role("link", name=product_name)
        )
        btn_wishlist = product_container.get_by_role(
            "button", name=ButtonNames.ADD_TO_WISH_LIST, exact=False
        ).or_(
            product_container.locator(
                f"button[data-original-title='{ButtonNames.ADD_TO_WISH_LIST}']"
            )
        )
        self.click(btn_wishlist.first)
        return product_name

    def get_success_message(self):
        """Return the success message locator."""
        return self.success_msg

    def click_wishlist_link_in_success_message(self):
        """Click on the 'wish list!' link in the success message."""
        self.click(self.lnk_wishlist_success)
        return WishlistPage(self.page)

    # ===== Product Count =====

    def get_product_count(self):
        """Returns all product locators found in search results."""
        return self.search_products
