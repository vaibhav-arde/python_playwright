# pages/my_account_page.py
# =====================
# Page Object for the My Account Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.logout_page import LogoutPage


class MyAccountPage(BasePage):
    """Page Object Model class for the My Account Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.msg_heading = page.locator('h2:has-text("My Account")')
        self.lnk_logout = page.locator("text='Logout'").nth(1)
        self.newsletter_subscription=page.locator("a:has-text('Subscribe / unsubscribe to newsletter')")
        self.radio_newsletter_yes = page.locator('input[name="newsletter"][value="1"]')
        self.radio_newsletter_no = page.locator('input[name="newsletter"][value="0"]')

    # ===== Page Validation Methods =====

    def get_my_account_page_heading(self):
        """Returns the locator for the 'My Account' page heading."""
        return self.msg_heading

    # ===== Logout Action =====

    def click_logout(self) -> LogoutPage:
        """Click on the 'Logout' link and return a LogoutPage instance."""
        self.click(self.lnk_logout)
        return LogoutPage(self.page)

    # ===== Page Title Verification =====

    def get_page_title(self) -> str:
        """Returns the title of the current page."""
        return self.get_title()

    # ===== Newsletter Subscription Action =====
    def click_newsletter_subscription(self):
        """Click on the 'Subscribe / unsubscribe to newsletter' link."""
        self.newsletter_subscription.click()
