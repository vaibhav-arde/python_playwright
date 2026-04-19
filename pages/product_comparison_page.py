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

        # ===== Breadcrumb Locators =====
        # ul.breadcrumb pins the container via CSS class. We avoid get_by_role("list")
        # because Bootstrap's "list-style: none" strips the implicit ARIA role from
        # <ul> and <li> in Chrome/Safari — making role-based queries return nothing.
        self.breadcrumb = page.locator("ul.breadcrumb")
        # The Home <a> contains only a FontAwesome icon (<i class="fa fa-home">)
        # with no text or aria-label, so get_by_role("link", name="Home") won't match.
        # CSS :has() scopes the match by structural child — more resilient than href.
        self.breadcrumb_home_link = self.breadcrumb.locator("li:has(a:has(i.fa-home))")
        # Inner <a> for dispatch_event click to bypass CSS pointer-event interception.
        self._breadcrumb_home_anchor = self.breadcrumb.locator("a:has(i.fa-home)")
        # Current page item — scoped to <li> to avoid matching the page <h1>.
        self.breadcrumb_current = self.breadcrumb.locator("li").filter(
            has_text="Product Comparison"
        )

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
        """Click the Home icon link in the breadcrumb.

        Both .click() and .click(force=True) fail here: Bootstrap's breadcrumb
        applies CSS pointer-events that swallow pointer-based events on the <li>,
        even when Playwright's actionability checks are skipped.
        dispatch_event("click") injects a JS MouseEvent directly into the DOM
        event system — CSS pointer-events cannot intercept it.
        """
        self.dispatch_event(self._breadcrumb_home_anchor, "click")

    # ===== Product Presence in Table =====

    def get_product_name_in_table(self, product_name: str):
        """Return the locator for the exact product name cell in the comparison table."""
        return self.page.get_by_role("cell").filter(
            has_text=re.compile(rf"^{re.escape(product_name)}$")
        )

    def get_product_image_in_table(self, product_name: str):
        """Return the product image locator scoped to the product's column."""
        return self.page.get_by_role("img", name=product_name)

    def get_product_price_in_table(self):
        """Return the price cell locator in the Product Comparison table.

        Finds the table row whose header td contains 'Price', then returns
        the last td — sufficient when exactly one product is in the table.
        """
        return (
            self.page.locator("table tr")
            .filter(has=self.page.locator("td", has_text=re.compile(r"^Price$")))
            .locator("td")
            .last
        )

    def get_all_price_cells_in_table(self):
        """Return all product price td locators in the Price row."""
        price_row = self.page.locator("table tr").filter(
            has=self.page.locator("td", has_text=re.compile(r"^Price$"))
        )
        return price_row.locator("td ~ td")

    def get_add_to_cart_button_in_table(self):
        """Return the 'Add to Cart' input button inside the comparison table."""
        return self.page.locator("table input.btn-primary[value='Add to Cart']")

    def get_remove_link_in_table(self):
        """Return the 'Remove' link locator inside the comparison table.

        Rendered as <a class='btn btn-danger btn-block'>Remove</a>.
        """
        return self.page.locator("table").get_by_role("link", name="Remove", exact=True)
