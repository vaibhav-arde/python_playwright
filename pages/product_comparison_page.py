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
        self.success_message = page.locator("div.alert.alert-success.alert-dismissible")

        # ===== Breadcrumb Locators =====
        self.breadcrumb = page.locator("ul.breadcrumb")
        self.breadcrumb_home_link = self.breadcrumb.locator("li:has(a:has(i.fa-home))")
        self._breadcrumb_home_anchor = self.breadcrumb.locator("a:has(i.fa-home)")
        self.breadcrumb_current = self.breadcrumb.locator("li").filter(
            has_text="Product Comparison"
        )

        # ===== Table UI Locators =====
        self.comparison_table = page.locator("table.table-bordered")

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

    # ===== Breadcrumb =====

    def get_breadcrumb(self):
        """Return the breadcrumb container locator."""
        return self.breadcrumb

    def get_breadcrumb_home_link(self):
        """Return the Home breadcrumb link locator."""
        return self.breadcrumb_home_link

    def get_breadcrumb_current_item(self):
        """Return the 'Product Comparison' breadcrumb item locator (current page)."""
        return self.breadcrumb_current

    def click_breadcrumb_home(self):
        """Click the Home icon link in the breadcrumb."""
        self.dispatch_event(self._breadcrumb_home_anchor, "click")

    # ===== Product Presence in Table =====

    def get_product_name_in_table(self, product_name: str):
        """Return the locator for the exact product name cell in the comparison table."""
        return self.page.get_by_role("cell").filter(
            has_text=re.compile(rf"^{re.escape(product_name)}$")
        )

    def get_product_image_in_table(self, product_name: str):
        """Return the product image locator scoped to the comparison table."""
        return self.page.locator("table").get_by_role("img", name=product_name, exact=True)

    def get_product_price_in_table(self):
        """Return the price cell locator in the Product Comparison table."""
        return (
            self.page.locator("table tr")
            .filter(has=self.page.locator("td", has_text=re.compile(r"^Price$")))
            .locator("td")
            .last
        )

    def get_all_price_cells_in_table(self):
        """Return all product price td locators in the Price row."""
        price_row = self.page.locator("table tr").filter(
            has=self.page.locator("td", has_text=re.compile(r"^Product$"))
        )
        return price_row.locator("td ~ td")

    def get_add_to_cart_button_in_table(self):
        """Return the 'Add to Cart' input button inside the comparison table."""
        return self.page.locator("table input.btn-primary[value='Add to Cart']")

    def get_remove_link_in_table(self):
        """Return the 'Remove' link locator inside the comparison table."""
        return self.page.locator("table").get_by_role("link", name="Remove", exact=True)

    # ===== Success Message =====

    def get_success_message(self) -> str:
        """Return the success message shown after a successful action."""
        self.wait_for(self.success_message, state="visible")
        return self.get_text(self.success_message)

    # ===== UI Checklist Methods =====

    def get_row_header(self, header_name: str):
        """Return the locator for a row header (first column) in the comparison table."""
        return self.comparison_table.locator("tr td:first-child").filter(
            has_text=re.compile(rf"^{re.escape(header_name)}$")
        )

    # ===== Cart & Removal Interaction =====

    def _get_column_index_for_product(self, product_name: str) -> int:
        """Find the column index for a specific product name in the comparison table."""
        product_name_row = (
            self.page.locator("table tr")
            .filter(has=self.page.locator("td", has_text=re.compile(r"^Product$")))
            .first
        )

        header_cells = product_name_row.locator("td")
        count = header_cells.count()

        for i in range(count):
            cell_text = header_cells.nth(i).inner_text().strip()
            if product_name in cell_text:
                return i
        return -1

    def click_add_to_cart_for_product(self, product_name: str):
        """Click the 'Add to Cart' button for a specific product in the comparison table."""
        target_index = self._get_column_index_for_product(product_name)

        if target_index != -1:
            button_row = (
                self.page.locator("table tr")
                .filter(has=self.page.locator("input[value='Add to Cart']"))
                .first
            )
            self.click(button_row.locator("td").nth(target_index).locator("input"))
        else:
            raise ValueError(
                messages.ERR_PRODUCT_NOT_FOUND_IN_COMPARISON.format(product_name=product_name)
            )

    def click_remove_for_product(self, product_name: str):
        """Click the 'Remove' link for a specific product in the comparison table."""
        target_index = self._get_column_index_for_product(product_name)

        if target_index != -1:
            remove_row = (
                self.page.locator("table tr")
                .filter(has=self.page.locator("a", has_text="Remove"))
                .first
            )
            self.click(remove_row.locator("td").nth(target_index).locator("a"))
        else:
            raise ValueError(
                messages.ERR_PRODUCT_NOT_FOUND_IN_COMPARISON.format(product_name=product_name)
            )
