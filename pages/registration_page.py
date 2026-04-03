# pages/registration_page.py
# =====================
# Page Object for the Registration Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page, expect, Locator

from pages.base_page import BasePage
from utils import messages


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
        self.radio_newsletter_yes = page.locator('input[name="newsletter"][value="1"]')
        self.radio_newsletter_no = page.locator('input[name="newsletter"][value="0"]')
        self.btn_continue = page.locator('input[value="Continue"]')
        self.msg_confirmation = page.locator('h1:has-text("Your Account Has Been Created!")')
        self.lbl_page_heading = page.get_by_role("heading", name="Register Account")
        self.msg_privacy_policy_warning = page.locator(".alert-danger")
        self.lnk_breadcrumb = page.locator("#account-register ul.breadcrumb")

        # ===== Warning / Validation Message Locators =====
        self.warn_privacy_policy = page.locator(".alert-danger")

        # ===== Error Message Locators =====
        self.err_privacy_policy = page.locator("div.alert-danger")
        self.err_firstname = page.locator("#input-firstname + .text-danger")
        self.err_lastname = page.locator("#input-lastname + .text-danger")
        self.err_email = page.locator("#input-email + .text-danger")
        self.err_telephone = page.locator("#input-telephone + .text-danger")
        self.err_password = page.locator("#input-password + .text-danger")
        self.password_mismatch_error = page.get_by_text(messages.WARN_PASSWORD_MISMATCH)
        self.err_email_already_exist = page.get_by_text(messages.WARN_EMAIL_ALREADY_EXISTS)

    # ===== Action Methods =====

    def set_first_name(self, fname: str):
        """Enter the user's first name."""
        self.txt_firstname.fill(fname)

    def set_last_name(self, lname: str):
        """Enter the user's last name."""
        self.txt_lastname.fill(lname)

    def set_email(self, email: str):
        """Enter the user's email address."""
        self.txt_email.fill(email)

    def set_telephone(self, tel: str):
        """Enter the user's telephone number."""
        self.txt_telephone.fill(tel)

    def set_password(self, pwd: str):
        """Enter the password."""
        self.txt_password.fill(pwd)

    def set_confirm_password(self, pwd: str):
        """Re-enter the password in the Confirm Password field."""
        self.txt_confirm_password.fill(pwd)

    def set_privacy_policy(self):
        """Select the Privacy Policy checkbox."""
        self.check(self.chk_policy)

    def set_newsletter_subscription(self, locator: str | Locator):
        self.check(locator)

    def click_continue(self):
        """Click the Continue button to submit the registration form."""
        self.click(self.btn_continue)

    def get_confirmation_msg(self):
        """Return the confirmation message locator."""
        return self.msg_confirmation

    def get_page_heading(self):
        return self.lbl_page_heading

    def get_breadcrumb(self):
        return self.lnk_breadcrumb  

    def get_privacy_policy_warning(self):
        """Return the privacy policy warning message locator."""
        return self.msg_privacy_policy_warning

    def get_password_field_type(self):
        """Return the type attribute of the password field."""
        return self.txt_password.get_attribute("type")

    def get_confirm_password_field_type(self):
        """Return the type attribute of the confirm password field."""
        return self.txt_confirm_password.get_attribute("type")

    # ===== Combined Workflow =====

    def complete_registration(self, user_data: dict, newsletter_locator: str | Locator = None):
        """Complete the full registration process using a data dictionary."""
        self.set_first_name(user_data["firstName"])
        self.set_last_name(user_data["lastName"])
        self.set_email(user_data["email"])
        self.set_telephone(user_data["telephone"])
        self.set_password(user_data["password"])
        self.set_confirm_password(user_data["password"])
        if newsletter_locator:
            self.set_newsletter_subscription(newsletter_locator)
        self.set_privacy_policy()
        self.click_continue()
        return self.msg_confirmation
