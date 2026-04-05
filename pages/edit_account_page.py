# pages/edit_account_page.py
# =====================
# Page Object for the Edit Account Information Page.
# Used to verify persisted user details after registration.

from playwright.sync_api import Page
from pages.base_page import BasePage


class EditAccountPage(BasePage):
    """Page Object Model for the Edit Account Information page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.txt_firstname = page.locator("#input-firstname")
        self.txt_lastname = page.locator("#input-lastname")
        self.txt_email = page.locator("#input-email")
        self.txt_telephone = page.locator("#input-telephone")

    # ===== Accessor Methods =====

    def get_first_name(self) -> str:
        """Returns the value in the First Name field."""
        return self.txt_firstname.input_value()

    def get_last_name(self) -> str:
        """Returns the value in the Last Name field."""
        return self.txt_lastname.input_value()

    def get_email(self) -> str:
        """Returns the value in the E-Mail field."""
        return self.txt_email.input_value()

    def get_telephone(self) -> str:
        """Returns the value in the Telephone field."""
        return self.txt_telephone.input_value()
