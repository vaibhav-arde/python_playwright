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
        self.btn_continue = page.get_by_role("button", name="Continue")
        self.txt_first_name = page.get_by_label("First Name")
        self.txt_last_name = page.get_by_label("Last Name")
        self.txt_address1 = page.get_by_label("Address 1")
        self.txt_address2 = page.get_by_label("Address 2")
        self.txt_city = page.get_by_label("City")
        self.txt_pin = page.get_by_label("Postcode")
        self.drp_country = page.get_by_label("Country")
        self.drp_state = page.get_by_label("State")
        self.btn_continue_billing_address = page.get_by_role("button", name="Continue")
        self.btn_continue_delivery_address = page.get_by_role("button", name="Continue")
        self.txt_delivery_method = page.get_by_label("Comments")
        self.btn_continue_shipping_address = page.get_by_role("button", name="Continue")
        self.chkbox_terms = page.get_by_label("I agree to the terms and conditions")
        self.btn_continue_payment_method = page.get_by_role("button", name="Continue")
        self.lbl_total_price = page.locator('strong:has-text("Total:") + td')
        self.btn_conf_order = page.get_by_role("button", name="Confirm")
        self.lbl_order_con_msg = page.get_by_role("heading")

    # ===== Page Validation =====

    def get_checkout_page_title(self) -> str:
        """Return the title of the Checkout page."""
        return self.get_title()

    # ===== Checkout Option =====

    def choose_checkout_option(self, checkout_option: str):
        """Choose the checkout type (e.g., Guest Checkout)."""
        if checkout_option.lower() == "guest checkout":
            self.click(self.radio_guest)

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
        """Click the Confirm Order button."""
        self.click(self.btn_conf_order)

    def is_order_placed(self):
        """Verify if the order confirmation message appears."""
        self.page.on("dialog", lambda dialog: dialog.accept())
        return self.lbl_order_con_msg
