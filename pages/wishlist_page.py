# pages/wishlist_page.py
# =====================
# Page Object for the Wishlist Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page, Locator

from pages.base_page import BasePage
from utils.constants import BreadcrumbOptionNames


class WishlistPage(BasePage):
    """Page Object Model class for the Wishlist Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.wishlist_page_heading = page.locator("#content h2")
        self.msg_empty_wishlist = page.locator("#content p")
        self.wishlist_table = page.locator("table.table-bordered.table-hover")
        self.wishlist_rows = self.wishlist_table.locator("tbody tr")
        self.btn_continue = page.get_by_role("link", name="Continue", exact=True)
        self.breadcrumb = page.locator(".breadcrumb")
        self.lnk_breadcrumb_home = self.breadcrumb.locator("li").nth(0).get_by_role("link")
        self.lnk_breadcrumb_account = self.breadcrumb.get_by_role(
            "link", name=BreadcrumbOptionNames.ACCOUNT, exact=True
        )
        self.lnk_breadcrumb_wishlist = self.breadcrumb.get_by_role(
            "link", name=BreadcrumbOptionNames.MY_WISH_LIST, exact=True
        )

    # ===== Wishlist Interactions =====

    def get_wishlist_page_heading(self) -> Locator:
        """Return the My Wish List page heading locator."""
        return self.wishlist_page_heading

    def get_home_breadcrumb_link(self) -> Locator:
        """Return the home breadcrumb link locator."""
        return self.lnk_breadcrumb_home

    def get_account_breadcrumb_link(self) -> Locator:
        """Return the account breadcrumb link locator."""
        return self.lnk_breadcrumb_account

    def get_wishlist_breadcrumb_link(self) -> Locator:
        """Return the wishlist breadcrumb link locator."""
        return self.lnk_breadcrumb_wishlist

    def get_empty_wishlist_message(self) -> Locator:
        """Return the empty wishlist message locator."""
        return self.msg_empty_wishlist

    def get_continue_button(self) -> Locator:
        """Return the Continue button locator."""
        return self.btn_continue

    def is_product_in_wishlist(self, product_name: str) -> Locator:
        """Check if a specific product is displayed in the wishlist and return its locator."""
        return self.wishlist_table.get_by_role("cell", name=product_name).first

    def click_home_breadcrumb(self):
        """Click the home breadcrumb link and return HomePage instance."""
        from pages.home_page import HomePage

        # The home breadcrumb is an icon-only link, so a small in-link offset is more reliable.
        self.lnk_breadcrumb_home.click(position={"x": 3, "y": 3})
        return HomePage(self.page)

    def click_account_breadcrumb(self):
        """Click the account breadcrumb link and return MyAccountPage instance."""
        from pages.my_account_page import MyAccountPage

        self.click(self.lnk_breadcrumb_account)
        return MyAccountPage(self.page)

    def click_wishlist_breadcrumb(self):
        """Click the wishlist breadcrumb link and stay on WishlistPage."""
        self.click(self.lnk_breadcrumb_wishlist)
        return WishlistPage(self.page)

    def click_continue_button(self):
        """Click Continue and return MyAccountPage instance."""
        from pages.my_account_page import MyAccountPage

        self.click(self.btn_continue)
        return MyAccountPage(self.page)
