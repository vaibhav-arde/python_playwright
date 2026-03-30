# pages/registration_page.py
# =====================
# Page Object for the Registration Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page

from pages.base_page import BasePage


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
        self.msg_confirmation = page.locator('h1:has-text("Your Account Has Been Created!")')

        # ===== Error Message Locators =====
        self.err_privacy_policy = page.locator("div.alert-danger")
        self.err_firstname = page.locator("#input-firstname + .text-danger")
        self.err_lastname = page.locator("#input-lastname + .text-danger")
        self.err_email = page.locator("#input-email + .text-danger")
        self.err_telephone = page.locator("#input-telephone + .text-danger")
        self.err_password = page.locator("#input-password + .text-danger")

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
        self.chk_policy.check()

    def click_continue(self):
        """Click the Continue button to submit the registration form."""
        self.btn_continue.click()

    def get_confirmation_msg(self):
        """Return the confirmation message locator."""
        return self.msg_confirmation

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
        return (
            self.err_privacy_policy.text_content()
            == "Warning: You must agree to the Privacy Policy!"
            and self.err_firstname.text_content()
            == "First Name must be between 1 and 32 characters!"
            and self.err_lastname.text_content() == "Last Name must be between 1 and 32 characters!"
            and self.err_email.text_content() == "E-Mail Address does not appear to be valid!"
            and self.err_telephone.text_content()
            == "Telephone must be between 3 and 32 characters!"
            and self.err_password.text_content() == "Password must be between 4 and 20 characters!"
        )
