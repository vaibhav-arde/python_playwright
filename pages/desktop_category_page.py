# pages/desktop_category_page.py
# =====================
# Page Object for the Desktops category page.
# Inherits from BasePage for reusable UI interaction methods.

import re
from playwright.sync_api import Page

from pages.base_page import BasePage


class DesktopCategoryPage(BasePage):
    """Page Object Model class for the Desktops category page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.category_page_header = page.get_by_role("heading", name="Desktops", exact=True)
        self.grid_view_button = page.locator("#grid-view")
        self.list_view_button = page.locator("#list-view")
        self.compare_success_message = page.locator("div.alert.alert-success.alert-dismissible")
        self.lnk_product_comparison = self.compare_success_message.get_by_role(
            "link", name="product comparison"
        )
        self.lnk_product_compare = page.get_by_role("link", name=re.compile(r"Product Compare"))
        self.product_cards = page.locator(".product-layout")

    # ===== Page Header =====

    def get_category_page_header(self):
        """Return the 'Desktops' category page heading locator."""
        return self.category_page_header

    # ===== View Selection =====

    def click_list_view(self):
        """Switch the desktops listing to list view."""
        self.click(self.list_view_button)

    def click_grid_view(self):
        """Switch the desktops listing to grid view."""
        self.click(self.grid_view_button)

    # ===== Product Verification =====

    def get_product_card(self, product_name: str):
        """Return the product card locator for a product in the category listing."""
        return self.product_cards.filter(has_text=product_name).first

    def get_first_product_card(self):
        """Return the first product card displayed in the category listing."""
        return self.product_cards.first

    def get_first_product_name(self) -> str:
        """Return the title text for the first visible product."""
        return self.get_text(self.get_first_product_card().locator("h4 a").first)

    # ===== Product Comparison in List View =====

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

    def click_product_compare_link(self):
        """Click the 'Product Compare' link located above the product listing."""
        self.click(self.lnk_product_compare)
