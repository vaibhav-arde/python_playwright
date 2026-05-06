# pages/sitemap_page.py
# =====================
# Page Object for the Site Map Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page

from pages.base_page import BasePage


class SitemapPage(BasePage):
    """Page Object Model class for the Site Map Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.lnk_password = page.get_by_role("link", name="Password", exact=True)

    # ===== Action Methods =====

    def click_password(self):
        """Click on the 'Password' link."""
        self.click(self.lnk_password)
