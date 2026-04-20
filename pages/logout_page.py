# pages/logout_page.py
# =====================
# Page Object for the Logout Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page

from pages.base_page import BasePage

class LogoutPage(BasePage):
    """Page Object Model class for the Logout Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        #Add logout page heading locator
        self.logout_heading = page.get_by_role("heading", name="Account Logout")
        self.btn_continue = page.locator(".btn.btn-primary")
        self.btn_login = page.locator("ul.dropdown-menu").get_by_role("link", name="Login")
        self.lnk_my_account = page.locator('span:has-text("My Account")')
        self.breadcrumb = page.locator("ul.breadcrumb")

    def get_expected_title(self) -> str:
        """Return the expected title for the Logout page."""
        return "Account Logout"

    def get_expected_url_pattern(self) -> str:
        """Return the expected URL route for the Logout page."""
        return r"route=account/logout"

    # ===== Action Methods =====

    def click_continue(self):
        """Click the 'Continue' button after logging out."""
        self.click(self.btn_continue)

    # Click dropdown menu from logout page
    def click_dropdown_logout_page(self):
        self.click(self.lnk_my_account)

    def get_continue_button(self):
        """Return the Continue button locator."""
        return self.btn_continue

    def logout(self):       
        # Click logout link from dropdown
        self.click(self.page.locator("ul.dropdown-menu").get_by_role("link", name="Logout"))
        self.click_continue()

    def verify_logout_page_heading(self):
        """Return the Account Logout heading locator."""
        return self.logout_heading

    def verify_login_btn_in_dropdown(self):
        return self.btn_login

    def get_breadcrumb(self):
        """Return the breadcrumb locator."""
        return self.breadcrumb

    def get_logout_page_title(self) -> str:
        """Return the precise page title for the Logout page."""
        return self.get_title()