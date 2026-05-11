# pages/shopping_cart_page.py
# =====================
# Page Object for the Shopping Cart Page.
# Inherits from BasePage for reusable UI interaction methods.

import re
from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.checkout_page import CheckoutPage
from utils import messages


class ShoppingCartPage(BasePage):
    """Page Object Model for the Shopping Cart Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        self.lbl_page_heading = page.get_by_role("heading", name=re.compile(r"Shopping Cart", re.IGNORECASE))
        self.lbl_total_price = page.locator("//*[@id='cart']/ul/li[2]/div/table/tbody/tr[4]/td[2]")
        self.btn_checkout = page.locator("a.btn.btn-primary")
        self.lbl_empty_cart_msg = page.locator("#content").get_by_text(messages.CART_EMPTY_TEXT)

    # ===== Methods =====

    def get_page_heading(self):
        """Return the 'Shopping Cart' heading locator."""
        return self.lbl_page_heading

    def click_product_image(self, product_name: str):
        """Click on the product image link for the given product name in the cart."""
        self.page.locator("table.table-bordered").locator("tr").filter(
            has=self.page.get_by_role("link", name=product_name, exact=True)
        ).locator("td.text-center img").click()

    def click_product_name(self, product_name: str):
        """Click on the product name link for the given product name in the cart."""
        self.page.locator("table.table-bordered").locator("td.text-left").get_by_role(
            "link", name=product_name, exact=True
        ).first.click()
    
    def clear_cart(self):
        """Removes all items from the shopping cart by clicking the Remove button for each item."""
        # The remove buttons have class 'btn-danger' and icons 'fa-times-circle'
        # Or they have title/data-original-title='Remove'
        remove_buttons = self.page.locator("button.btn-danger").filter(has=self.page.locator("i.fa-times-circle"))
        
        while remove_buttons.count() > 0:
            remove_buttons.first.click()
            # Wait for the item to be removed (usually the page reloads or the row disappears)
            self.page.wait_for_load_state("networkidle")
            # Re-locate as the page might have changed
            remove_buttons = self.page.locator("button.btn-danger").filter(has=self.page.locator("i.fa-times-circle"))

    def get_total_price(self):
        """Returns the total price element from the shopping cart."""
        return self.lbl_total_price

    def click_on_checkout(self) -> CheckoutPage:
        """Click on the Checkout button and navigate to CheckoutPage."""
        self.click(self.btn_checkout)
        return CheckoutPage(self.page)

    def is_page_loaded(self):
        """Verify if the Shopping Cart page is loaded."""
        return self.btn_checkout
