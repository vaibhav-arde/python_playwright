# pages/category_page.py
# =====================
# Page Object for Category and Sub-category Pages.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page
from pages.base_page import BasePage


class CategoryPage(BasePage):
    """Page Object Model class for Category and Sub-category pages."""

    def __init__(self, page: Page):
        super().__init__(page)

    def select_subcategory_from_sidebar(self, subcategory_name: str):
        """Select a subcategory from the left-hand sidebar menu."""
        # Using a more robust locator for the list group items
        locator = self.page.locator("a.list-group-item").filter(has_text=subcategory_name)
        self.click(locator)

    def add_product_to_wishlist(self, product_name: str):
        """
        Click on 'Add to Wish List' for a specific product in the category grid.
        Returns the product name for verification.
        """
        # Locate the product layout container by filtering for the product name link
        product_container = self.page.locator(".product-layout").filter(
            has=self.page.get_by_role("link", name=product_name)
        )

        # Click the wishlist button (index 1 in the button group)
        btn_wishlist = product_container.get_by_role("button").nth(1)
        self.click(btn_wishlist)
        return product_name
