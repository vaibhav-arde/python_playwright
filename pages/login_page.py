# pages/login_page.py
# =====================
# Page Object for the Login Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page, Locator

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object Model class for the Login Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.txt_email = page.locator("#input-email")
        self.txt_password = page.locator("#input-password")
        self.btn_login = page.locator("input[value='Login']")
        self.msg_login_error = page.locator(".alert-danger")

    def get_title(self) -> str:
        """Return the expected title for the Login page."""
        return "Account Login"

    def get_url_pattern(self) -> str:
        """Return the expected URL route for the Login page."""
        return r".*account/login"

    # ===== Action Methods =====

    def set_email(self, email: str):
        """Enter the user's email address."""
        self.fill(self.txt_email, email)

    def set_password(self, pwd: str):
        """Enter the password."""
        self.fill(self.txt_password, pwd)

    def click_login(self):
        """Click the Login button."""
        self.click(self.btn_login)

    def get_login_error(self) -> Locator:
        """Return the login error message locator."""
        return self.msg_login_error

    # ===== Combined Workflow =====

    def login(self, email: str, pwd: str):
        """Complete the full login process."""
        self.set_email(email)
        self.set_password(pwd)
        self.click_login()

    def verify_login_btn_visible(self):
        return self.btn_login
