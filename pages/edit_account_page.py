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
        self.txt_firstname = page.get_by_label("First Name")
        self.txt_lastname = page.get_by_label("Last Name")
        self.txt_email = page.get_by_label("E-Mail")
        self.txt_telephone = page.get_by_label("Telephone")

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
