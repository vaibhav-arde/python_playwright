# pages/site_map_page.py
# =====================
# Page Object for the Site Map Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page
from pages.base_page import BasePage


class SiteMapPage(BasePage):
    """Page Object Model class for the Site Map Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.lnk_search = page.get_by_role("link", name="Search", exact=True)

    # ===== Action Methods =====

    def click_search_link(self):
        """Click on the 'Search' link from the Site Map page."""
        self.click(self.lnk_search)
