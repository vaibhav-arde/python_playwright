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
        self.msg_heading = page.get_by_role("heading", name="My Account Information")
        self.btn_continue = page.get_by_role("button", name="Continue")
        self.msg_success = page.locator("div.alert-success")

    def get_page_heading(self):
        """Returns the page heading locator."""
        return self.msg_heading

    def get_page_title(self) -> str:
        """Returns the page title."""
        return self.get_title()

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
        return self.txt_telephone.input_value()

    # ===== Actions =====

    def update_account_information(self, user):
        self.txt_firstname.fill(user["firstName"])
        self.txt_lastname.fill(user["lastName"])
        self.txt_email.fill(user["email"])
        self.txt_telephone.fill(user["telephone"])

    def click_continue(self):
        """Click on the Continue button."""
        self.click(self.btn_continue)

    def get_success_message(self):
        """Returns the success message locator."""
        return self.msg_success
