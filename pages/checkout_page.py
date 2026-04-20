# pages/checkout_page.py
# =====================
# Page Object for the Checkout Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Page Object Model class for the Checkout Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.radio_guest = page.get_by_label("Guest Checkout")
        self.btn_continue = page.locator("#button-account")
        self.txt_first_name = page.locator("#input-payment-firstname")
        self.txt_last_name = page.locator("#input-payment-lastname")
        self.txt_address1 = page.locator("#input-payment-address-1")
        self.txt_address2 = page.locator("#input-payment-address-2")
        self.txt_city = page.locator("#input-payment-city")
        self.txt_pin = page.locator("#input-payment-postcode")
        self.drp_country = page.locator("#input-payment-country")
        self.drp_state = page.locator("#input-payment-zone")
        self.btn_continue_billing_address = page.locator("#button-payment-address")
        self.btn_continue_delivery_address = page.locator("#button-shipping-address")
        self.txt_delivery_method = page.locator('textarea[name="comment"]')
        self.btn_continue_shipping_address = page.locator("#button-shipping-method")
        self.chkbox_terms = page.locator('input[name="agree"]')
        self.btn_continue_payment_method = page.locator("#button-payment-method")
        self.lbl_total_price = page.locator("tr:has(td strong:has-text('Total:')) td:last-child")
        self.btn_conf_order = page.locator("#button-confirm")
        self.lbl_order_con_msg = page.get_by_role("heading", level=1)
        self.lnk_product_name_confirm = page.locator("#collapse-checkout-confirm table tbody tr td.text-left a").first

    # ===== Page Validation =====

    def get_checkout_page_title(self) -> str:
        """Return the title of the Checkout page."""
        return self.get_title()

    # ===== Checkout Option =====

    def choose_checkout_option(self, checkout_option: str):
        """Choose the checkout type (e.g., Guest Checkout)."""
        if checkout_option.lower() == "guest checkout":
            self.radio_guest.click()

    def click_continue(self):
        """Click the Continue button after choosing checkout option."""
        self.click(self.btn_continue)

    # ===== Billing Details =====

    def set_first_name(self, first_name: str):
        self.fill(self.txt_first_name, first_name)

    def set_last_name(self, last_name: str):
        self.fill(self.txt_last_name, last_name)

    def set_address1(self, address1: str):
        self.fill(self.txt_address1, address1)

    def set_address2(self, address2: str):
        self.fill(self.txt_address2, address2)

    def set_city(self, city: str):
        self.fill(self.txt_city, city)

    def set_pin(self, pin: str):
        self.fill(self.txt_pin, pin)

    def set_country(self, country: str):
        """Select a country from the dropdown."""
        self.select_option(self.drp_country, label=country)

    def set_state(self, state: str):
        """Select a state/region from the dropdown."""
        self.select_option(self.drp_state, label=state)

    # ===== Continue Buttons =====

    def click_continue_after_billing_address(self):
        """Click Continue after entering billing address."""
        self.click(self.btn_continue_billing_address)

    def click_continue_after_delivery_address(self):
        """Click Continue after confirming delivery address."""
        self.click(self.btn_continue_delivery_address)

    # ===== Delivery Method =====

    def set_delivery_method_comment(self, message: str):
        """Enter a comment for delivery."""
        self.fill(self.txt_delivery_method, message)

    def click_continue_after_delivery_method(self):
        """Click Continue after setting delivery method."""
        self.click(self.btn_continue_shipping_address)

    # ===== Payment Method =====

    def select_terms_and_conditions(self):
        """Check the Terms & Conditions checkbox."""
        self.check(self.chkbox_terms)

    def click_continue_after_payment_method(self):
        """Click Continue after selecting payment method."""
        self.click(self.btn_continue_payment_method)

    # ===== Order Confirmation =====

    def get_total_price_before_confirm(self):
        """Return the total price before placing the order."""
        return self.lbl_total_price

    def click_confirm_order(self):
        """Click the Confirm Order button and handle the resulting alert dialog."""
        # Dialogs must be handled by a listener set up BEFORE the action
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.click(self.btn_conf_order)

    def is_order_placed(self):
        """Verify if the order confirmation message appears."""
        return self.lbl_order_con_msg

    def click_product_name_confirm(self) -> "ProductPage":
        """Click on the product name link in the confirm order section and return ProductPage instance."""
        from pages.product_page import ProductPage
        self.click(self.lnk_product_name_confirm)
        return ProductPage(self.page)
