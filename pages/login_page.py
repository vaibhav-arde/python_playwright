# pages/login_page.py
# =====================
# Page Object for the Login Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object Model class for the Login Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.txt_email_address = page.locator("#input-email")
        self.txt_password = page.locator("#input-password")
        self.btn_login = page.locator('input[value="Login"]')
        self.txt_error_message = page.locator(".alert.alert-danger.alert-dismissible")
        self.btn_continue = page.get_by_role("link", name="Continue")
        self.lnk_register_right = page.get_by_role("link", name="Register")

    # ===== Action Methods =====

    def set_email(self, email: str):
        """Enter the email address in the Email field."""
        self.txt_email_address.fill(email)

    def set_password(self, password: str):
        """Enter the password in the Password field."""
        self.txt_password.fill(password)

    def click_login(self):
        """Click the Login button."""
        self.btn_login.click()

    def login(self, email: str, password: str):
        """Perform the complete login operation."""
        self.set_email(email)
        self.set_password(password)
        self.click_login()

    def get_login_error(self):
        """Return the error message element if login fails."""
        return self.txt_error_message

    def click_continue(self):
        self.btn_continue.click()

    def click_right_column_register(self):
        self.lnk_register_right.click()
