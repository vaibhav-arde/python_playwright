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
        self.btn_continue = page.locator('input[value="Continue"], a.btn.btn-primary:has-text("Continue")')
        self.msg_confirmation = page.locator('h1:has-text("Your Account Has Been Created!")')
        self.lbl_page_heading = page.get_by_role("heading", name="Register Account")
        self.msg_privacy_policy_warning = page.locator("#account-register > div.alert.alert-danger.alert-dismissible")
        self.lnk_login = page.get_by_role("link", name="Login")
        self.lnk_breadcrumb = page.locator("#account-register ul.breadcrumb")
        self.login_page_link = page.get_by_role("link", name="login page")

        # ===== Error Message Locators =====
        self.err_privacy_policy = page.locator("div.alert-danger")
        self.err_firstname = page.locator("#input-firstname + .text-danger")
        self.err_lastname = page.locator("#input-lastname + .text-danger")
        self.err_email = page.locator("#input-email + .text-danger")
        self.err_telephone = page.locator("#input-telephone + .text-danger")
        self.err_password = page.locator("#input-password + .text-danger")
        self.password_mismatch_error = page.get_by_text(messages.WARN_PASSWORD_MISMATCH)
        self.err_email_already_exist = page.get_by_text(messages.WARN_EMAIL_ALREADY_EXISTS)
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

    def set_newsletter_subscription(self, is_yes: bool = True, newsletter_locator: Locator = None):
        """Select newsletter subscription option."""
        if newsletter_locator:
            self.check(newsletter_locator)
        elif is_yes:
            self.check(self.radio_newsletter_yes)
        else:
            self.check(self.radio_newsletter_no)

    def click_continue(self):
        """Click the Continue button to submit the registration form."""
        self.click(self.btn_continue)

    def click_login_link(self):
        """Click on the 'Login' link in the Register page."""
        self.click(self.lnk_login)

    def click_login_page_link(self):
        """Click on the 'Login Page' link."""
        self.click(self.login_page_link)

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

    def get_privacy_policy_warning(self):
        """Return the Privacy Policy alert warning locator."""
        return self.msg_privacy_policy_warning

    # ===== Combined Workflow =====

    def complete_registration(self, user_data: dict, subscribe_newsletter: bool = False, newsletter_locator: Locator = None):
        """Complete the full registration process using a data dictionary."""
        self.set_first_name(user_data["firstName"])
        self.set_last_name(user_data["lastName"])
        self.set_email(user_data["email"])
        self.set_telephone(user_data["telephone"])
        self.set_password(user_data["password"])
        self.set_confirm_password(user_data["password"])
        if newsletter_locator:
            self.set_newsletter_subscription(newsletter_locator=newsletter_locator)
        elif subscribe_newsletter:
            self.set_newsletter_subscription(is_yes=True)
        self.set_privacy_policy()
        self.click_continue()
        return self.msg_confirmation

    def error_msg_visible(self):
        """Assert that all mandatory field error messages are visible."""
        expect(self.err_privacy_policy).to_be_visible()
        expect(self.err_firstname).to_be_visible()
        expect(self.err_lastname).to_be_visible()
        expect(self.err_email).to_be_visible()
        expect(self.err_telephone).to_be_visible()
        expect(self.err_password).to_be_visible()
