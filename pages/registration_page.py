# pages/registration_page.py
# =====================
# Page Object for the Registration Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page, expect, Locator

from pages.base_page import BasePage
from utils.message import Message
from pages.my_account_page import MyAccountPage
from pages.newsletter_page import NewsletterPage


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
        self.radio_yes = page.locator('input[name="newsletter"][value="1"]')
        self.radio_no = page.locator('input[name="newsletter"][value="0"]')
        self.msg_confirmation = page.locator('h1:has-text("Your Account Has Been Created!")')
        self.lnk_continue = page.get_by_role("link", name="Continue")

        # ===== Error Message Locators =====
        self.err_privacy_policy = page.locator("div.alert-danger")
        self.err_firstname = page.locator("#input-firstname + .text-danger")
        self.err_lastname = page.locator("#input-lastname + .text-danger")
        self.err_email = page.locator("#input-email + .text-danger")
        self.err_telephone = page.locator("#input-telephone + .text-danger")
        self.err_password = page.locator("#input-password + .text-danger")
        self.password_mismatch_error = page.get_by_text(Message.password_not_match_error)
        self.err_email_already_exist = page.get_by_text(Message.email_already_exist_error)

        # ===== Warning / Validation Message Locators =====
        self.warn_privacy_policy = page.locator(".alert-danger")

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

    def set_newsletter(self, value: str):
        newsletter_page = NewsletterPage(self.page)
        newsletter_page.set_newsletter(value)

    def set_newsletter_subscription(self, locator: str | Locator):
        self.check(locator)

    def click_continue(self):
        self.click(self.btn_continue)

    def get_confirmation_msg(self):
        """Return the confirmation message locator."""
        return self.msg_confirmation

    def get_password_mismatch_error(self):
        """Return the password mismatch error message locator."""
        return self.password_mismatch_error

    def get_email_already_exist_error(self):
        """Return the email already exist error message locator."""
        return self.err_email_already_exist

    def get_email_validation_message(self) -> str:
        """Return the native browser validation message for the email input."""
        return self.txt_email.evaluate("node => node.validationMessage")

    def get_privacy_policy_warning(self) -> str:
        """Return the Privacy Policy alert warning text."""
        return self.get_text(self.warn_privacy_policy)
    # ===== My Account Page Navigation =====
    def click_continue_to_my_account(self):
        """Click Continue link and navigate to My Account page."""
        self.click(self.lnk_continue)
        return MyAccountPage(self.page)    

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

    def error_msg_visible(self):
        """check the error message visible or not for empty fields on click continue."""

        expect(self.err_privacy_policy).to_have_text(Message.privacy_policy_error)

        expect(self.err_firstname).to_have_text(Message.firstname_error)

        expect(self.err_lastname).to_have_text(Message.lastname_error)

        expect(self.err_email).to_have_text(Message.email_error)

        expect(self.err_telephone).to_have_text(Message.telephone_error)

        expect(self.err_password).to_have_text(Message.password_error)
