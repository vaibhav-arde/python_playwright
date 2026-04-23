# pages/home_page.py
# =====================
# Page Object for the Home Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.wishlist_page import WishlistPage
from pages.category_page import CategoryPage


class HomePage(BasePage):
    """Page Object Model class for the Home page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.lnk_my_account = page.locator('span:has-text("My Account")')
        self.lnk_register = page.locator('a:has-text("Register")')
        self.lnk_login = page.locator("ul.dropdown-menu").get_by_role("link", name="Login")
        self.txt_search_box = page.locator('input[placeholder="Search"]')
        self.btn_search = page.locator('#search button[type="button"]')
        self.lnk_logo = page.locator("#logo a")
        self.featured_section = page.locator("h3:has-text('Featured')")
        self.success_msg = page.locator(".alert-success")
        self.lnk_wishlist_success = self.success_msg.get_by_role("link", name="wish list")

    # ===== Action Methods =====

    def get_home_page_title(self) -> str:
        """Return the title of the Home Page."""
        return self.get_title()

    def click_my_account(self):
        """Click on the 'My Account' link."""
        self.click(self.lnk_my_account)

    def click_register(self):
        """Click on the 'Register' link under My Account."""
        self.click(self.lnk_register)

    def click_login(self):
        """Click on the 'Login' link under My Account."""
        self.click(self.lnk_login)

    def enter_product_name(self, product_name: str):
        """Enter the product name into the search input box."""
        self.fill(self.txt_search_box, product_name)

    def click_search(self):
        """Click on the search button to initiate the product search."""
        self.click(self.btn_search)

    def click_logo(self):
        """Click on the 'Store logo' (Your Store)."""
        self.click(self.lnk_logo)

    def scroll_to_featured_section(self):
        """Scroll down to the 'Featured' section."""
        self.featured_section.scroll_into_view_if_needed()

    def add_featured_product_to_wishlist(self, product_name: str):
        """
        Click on 'Add to Wish List' option for a product in the 'Featured' section.
        Identifies the product container by name and then clicks the heart icon.
        """
        # Locating the product container that contains the product name link
        product_container = self.page.locator(".product-layout").filter(
            has=self.page.get_by_role("link", name=product_name)
        )
        # Clicking the wishlist button (usually the second button in the group: cart, wishlist, compare)
        # We can use the title or the icon class. OpenCart uses title="Add to Wish List"
        btn_wishlist = product_container.get_by_role("button").nth(1)
        self.click(btn_wishlist)

    def get_success_message(self):
        """Return the success message locator."""
        return self.success_msg

    def click_wishlist_link_in_success_message(self):
        """Click on the 'wish list!' link in the success message."""
        self.click(self.lnk_wishlist_success)
        return WishlistPage(self.page)

    def open_category_menu(self, category_name: str):
        """Open a main category dropdown in the top navigation menu by clicking it."""
        locator = self.page.get_by_role("link", name=category_name, exact=True)
        self.click(locator)

    def click_show_all_in_category(self, category_name: str):
        """Click on the 'Show All [Category]' link in the dropdown menu."""
        # Using a CSS selector for the 'See All' link to be more robust against text spacing issues
        locator = self.page.locator("a.see-all").filter(has_text=f"Show All {category_name}")
        # If the exact text filter fails due to spacing, fall back to just the visible see-all link
        if not locator.is_visible():
            locator = self.page.locator("a.see-all").filter(has_text=category_name)

        locator.wait_for(state="visible")
        self.click(locator)
        return CategoryPage(self.page)
