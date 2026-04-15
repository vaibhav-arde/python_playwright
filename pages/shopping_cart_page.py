# pages/shopping_cart_page.py
# =====================
# Page Object for the Shopping Cart Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.checkout_page import CheckoutPage


class ShoppingCartPage(BasePage):
    """Page Object Model for the Shopping Cart Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.lbl_total_price = page.locator("//*[@id='cart']/ul/li[2]/div/table/tbody/tr[4]/td[2]")
        self.btn_checkout = page.locator("a.btn.btn-primary")
        self.warning_msg = page.locator("div.alert.alert-danger.alert-dismissible, div.alert.alert-danger")
        self.txt_cart_quantity = page.locator("input[name^='quantity']")

    # ===== Methods =====

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

    def get_warning_message(self):
        """Return the cart warning message locator."""
        return self.warning_msg

    def get_first_cart_quantity_value(self) -> str:
        """Return first product quantity value from cart table."""
        return self.txt_cart_quantity.first.get_attribute("value") or ""
