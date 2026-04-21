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
        self.txt_email_address = page.get_by_label("E-Mail Address")
        self.txt_password = page.get_by_label("Password")
        self.btn_login = page.get_by_role("button", name="Login")
        self.txt_error_message = page.locator(
            "#account-login .alert.alert-danger, .alert.alert-danger.alert-dismissible"
        )
        self.btn_continue = page.get_by_role("link", name="Continue")
        self.lnk_register_right = page.get_by_role("link", name="Register")

    # ===== Action Methods =====

    def set_email(self, email: str):
        """Enter the email address in the Email field."""
        self.fill(self.txt_email_address, email)

    def set_password(self, password: str):
        """Enter the password in the Password field."""
        self.fill(self.txt_password, password)

    def click_login(self):
        """Click the Login button."""
        self.click(self.btn_login)

    def login(self, email: str, password: str):
        """Perform the complete login operation."""
        self.set_email(email)
        self.set_password(password)
        self.click_login()

    def get_login_error(self):
        """Return the error message element if login fails."""
        return self.txt_error_message

    def click_continue(self):
        """Click the Continue button after logging out."""
        self.click(self.btn_continue)

    def click_right_column_register(self):
        """Click the Register button in the right column."""
        self.click(self.lnk_register_right)
