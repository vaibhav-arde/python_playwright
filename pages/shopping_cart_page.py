# pages/shopping_cart_page.py
# =====================
# Page Object for the Shopping Cart Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page
from pages.base_page import BasePage

class ShoppingCartPage(BasePage):
    """Page Object Model for the Shopping Cart Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.lbl_total_price = page.locator("#content tr:has(td strong:has-text('Total:')) td:last-child")
        self.btn_checkout = page.locator("#content").get_by_role("link", name="Checkout")
        self.warning_msg = page.locator("div.alert.alert-danger.alert-dismissible, div.alert.alert-danger")
        self.txt_cart_quantity = page.locator("#content input[name^='quantity']")
        self.lnk_product_image = page.locator(".table-responsive table tbody tr td.text-center a").first
        self.lnk_product_name = page.locator(".table-responsive table tbody tr td.text-left a").first

    # ===== Methods =====

    def click_product_image(self) -> "ProductPage":
        """Click on the product image link in the shopping cart and return ProductPage instance."""
        from pages.product_page import ProductPage
        self.click(self.lnk_product_image)
        return ProductPage(self.page)

    def click_product_name(self) -> "ProductPage":
        """Click on the product name link in the shopping cart and return ProductPage instance."""
        from pages.product_page import ProductPage
        self.click(self.lnk_product_name)
        return ProductPage(self.page)

    def get_total_price(self):
        """Returns the total price element from the shopping cart."""
        return self.lbl_total_price

    def click_on_checkout(self):
        """Click on the Checkout button and navigate to CheckoutPage."""
        from pages.checkout_page import CheckoutPage
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

    def clear_cart(self):
        """Remove all items from the shopping cart."""
        # Use selector for remove button (cross icon)
        remove_buttons = self.page.locator("button[data-original-title='Remove'], button[title='Remove']")
        while remove_buttons.count() > 0:
            target = remove_buttons.first
            target.click()
            # Wait for the element to be detached from DOM instead of full page load
            target.wait_for(state="detached", timeout=5000)
