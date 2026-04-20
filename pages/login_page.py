# pages/login_page.py
# =====================
# Page Object for the Login Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page

from pages.base_page import BasePage
from utils import messages


class LoginPage(BasePage):
    """Page Object Model class for the Login Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.txt_email_address = page.locator("#input-email")
        self.txt_password = page.locator("#input-password")
        self.btn_login = page.locator('input[value="Login"]')
        self.txt_error_message = page.get_by_text(messages.WARN_LOGIN_ERROR)
        self.txt_login_attempts_error = page.get_by_text(messages.WARN_LOGIN_ATTEMPTS_EXCEEDED)
        self.lnk_forgot_password = page.locator("#content").get_by_role("link", name=messages.FORGOT_PASSWORD)
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

    def get_login_attempts_error(self):
        """Return the error message element when login attempts are exceeded."""
        return self.txt_login_attempts_error

    def get_email_field(self):
        """Return the locator for the Email Address field."""
        return self.txt_email_address

    def get_password_field(self):
        """Return the locator for the Password field."""
        return self.txt_password

    def click_forgot_password(self):
        """Click the Forgot Password link."""
        self.click(self.lnk_forgot_password)

    def get_forgot_password(self):
        """Return the title of the forgot password page."""
        return self.lnk_forgot_password

    def login_with_keyboard(self, email: str, password: str):
        """Perform a login using only keyboard interactions."""
        # Tab until email field is focused and type email
        self.tab_until_focused(self.txt_email_address)
        self.page.keyboard.type(email)

        # Tab to password field and type password
        self.tab_until_focused(self.txt_password)
        self.page.keyboard.type(password)

        # Tab until login button is focused and press Enter
        self.tab_until_focused(self.btn_login)
        self.page.keyboard.press("Enter")

    def select_password_text_using_mouse(self):
        """Simulate selecting password text using Playwright's advanced select_text method."""
        self.txt_password.select_text()

    def right_click_password_field(self):
        """Right click the password field to open the native context menu."""
        self.txt_password.click(button="right")

    def select_password_text_using_keyboard(self):
        """Select text in the password field using keyboard shortcut (Ctrl+A)."""
        self.txt_password.focus()
        self.page.keyboard.press("Control+A")

    def copy_password_text_using_keyboard(self):
        """Attempt to copy text from password field using keyboard shortcut (Ctrl+C)."""
        self.page.keyboard.press("Control+C")

    def is_copy_allowed_from_password_field(self) -> bool:
        """Verify if copy is allowed from the password field natively."""
        return self.txt_password.evaluate("el => document.queryCommandSupported('copy') && document.queryCommandEnabled('copy') && el.type !== 'password'")