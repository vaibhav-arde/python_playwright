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
        self.btn_continue = page.get_by_role("button", name="Continue")

    # ===== Action Methods =====

    def click_continue(self):
        """Click the 'Continue' button after logging out."""
        self.click(self.btn_continue)

    def get_continue_button(self):
        """Return the Continue button locator."""
        return self.btn_continue
