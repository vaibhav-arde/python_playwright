# pages/registration_page.py
# =====================
# Page Object for the Registration Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page

from pages.base_page import BasePage
from utils.constants import Messages


class RegistrationPage(BasePage):
    """Page Object Model class for the Registration Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.txt_firstname = page.locator("#input-firstname")
        self.txt_lastname = page.locator("#input-lastname")
        self.txt_email = page.locator("#input-email")
        self.txt_telephone = page.locator("#input-telephone")
        self.txt_password = page.locator("#input-password")
        self.txt_confirm_password = page.locator("#input-confirm")
        self.chk_policy = page.locator('input[name="agree"]')
        self.btn_continue = page.locator('input[value="Continue"]')
        self.msg_confirmation = page.locator(
         f'h1:has-text("{Messages.REGISTRATION_SUCCESS}")'
)

    # ===== Action Methods =====

    def set_first_name(self, fname: str):
        """Enter the user's first name."""
        self.fill(self.txt_firstname, fname)

    def set_last_name(self, lname: str):
        """Enter the user's last name."""
        self.fill(self.txt_lastname, lname)

    def set_email(self, email: str):
        """Enter the user's email address."""
        self.fill(self.txt_email, email)

    def set_telephone(self, tel: str):
        """Enter the user's telephone number."""
        self.fill(self.txt_telephone, tel)

    def set_password(self, pwd: str):
        """Enter the password."""
        self.fill(self.txt_password, pwd)

    def set_confirm_password(self, pwd: str):
        """Re-enter the password in the Confirm Password field."""
        self.fill(self.txt_confirm_password, pwd)

    def set_privacy_policy(self):
        """Select the Privacy Policy checkbox."""
        self.check(self.chk_policy)

    def click_continue(self):
        """Click the Continue button to submit the registration form."""
        self.click(self.btn_continue)

    def get_confirmation_msg(self):
        """Return the confirmation message locator."""
        return self.msg_confirmation

    def fill_registration_form(self, fname: str, lname: str, email: str, telephone: str, password: str, confirm_password: str):
        """Fill all registration form fields with the provided values."""
        self.set_first_name(fname)
        self.set_last_name(lname)
        self.set_email(email)
        self.set_telephone(telephone)
        self.set_password(password)
        self.set_confirm_password(confirm_password)

    # ===== Combined Workflow =====

    def complete_registration(self, user_data: dict):
        """Complete the full registration process using a data dictionary."""
        self.set_first_name(user_data["firstName"])
        self.set_last_name(user_data["lastName"])
        self.set_email(user_data["email"])
        self.set_telephone(user_data["telephone"])
        self.set_password(user_data["password"])
        self.set_confirm_password(user_data["password"])
        self.set_privacy_policy()
        self.click_continue()
        return self.msg_confirmation
