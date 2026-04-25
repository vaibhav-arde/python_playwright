# pages/my_account_page.py
# =====================
# Page Object for the My Account Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.logout_page import LogoutPage
from pages.edit_account_page import EditAccountPage


class MyAccountPage(BasePage):
    """Page Object Model class for the My Account Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.msg_heading = page.locator('h2:has-text("My Account")')
        self.lnk_logout = page.locator("text='Logout'").nth(1)
        self.newsletter_subscription = page.locator(
            "a:has-text('Subscribe / unsubscribe to newsletter')"
        )
        self.radio_newsletter_yes = page.locator('input[name="newsletter"][value="1"]')
        self.radio_newsletter_no = page.locator('input[name="newsletter"][value="0"]')
        self.lnk_edit_account = page.locator('a:has-text("Edit your account information")')

        self.lnk_subscribe_unsubscribe_to_newsletter = page.locator("#column-right").get_by_role(
            "link", name="Newsletter"
        )
        self.msg_newsletter_heading = page.locator("h1:has-text('Newsletter')")
        self.lnk_change_password = page.locator("a:has-text('Change your password')")
        self.lnk_right_column_password = page.locator("#column-right").get_by_role(
            "link", name="Password"
        )

    # ===== Page Validation Methods =====

    def get_my_account_page_heading(self):
        """Returns the locator for the 'My Account' page heading."""
        return self.msg_heading

    def get_newsletter_page_heading(self):
        """Returns the locator for Newsletter page."""
        return self.msg_newsletter_heading

    def get_logout_link(self):
        """Returns the locator for the 'Logout' link."""
        return self.lnk_logout

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
        self.click(self.newsletter_subscription)

    # ===== Account Detail Actions =====
    def click_edit_account_info(self) -> EditAccountPage:
        """Click on 'Edit your account information' and return EditAccountPage instance."""
        self.click(self.lnk_edit_account)
        return EditAccountPage(self.page)

    # ===== Password Change Actions =====
    def click_change_password_link(self):
        """Click on 'Change your password' link."""
        self.click(self.lnk_change_password)

    def click_password_right_column(self):
        """Click on the 'Password' link in the right column."""
        self.click(self.lnk_right_column_password)
