# pages/home_page.py
# =====================
# Page Object for the Home Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.login_page import LoginPage


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
        self.lnk_logout = page.locator('a:has-text("Logout")')
        self.lnk_contact_us = page.get_by_role("link", name="Contact Us")
        self.lnk_desktops = page.get_by_role("link", name="Desktops")
        self.lnk_show_all_desktops = page.get_by_role("link", name="Show AllDesktops")
        self.dropdown = page.locator("a.dropdown-toggle").filter(has_text="My Account")
        self.lnk_sitemap = page.get_by_role("link", name="Site Map")
        self.lnk_account_information = page.get_by_role("link", name="Account Information")

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
        return LoginPage(self.page)

    def enter_product_name(self, product_name: str):
        """Enter the product name into the search input box."""
        self.fill(self.txt_search_box, product_name)

    def click_search(self):
        """Click on the search button to initiate the product search."""
        self.click(self.btn_search)

    def click_contact_us(self):
        """Click on the Contact Us link in the footer."""
        self.click(self.lnk_contact_us)

    def click_desktops_category(self):
        """Click on the Desktops category link."""
        self.click(self.lnk_desktops)

    def logout_link(self):
        """Click on the 'Logout' link."""
        return self.lnk_logout

    def is_dropdown_menu_visible(self) -> bool:
        """Check if the dropdown menu is visible."""
        return self.dropdown

    def click_show_all_desktops(self):
        """Click on the 'Show All Desktops' link."""
        self.click(self.lnk_show_all_desktops)

    def click_sitemap(self):
        """Click on the 'Site Map' link in the footer."""
        self.click(self.lnk_sitemap)

    def click_account_information(self):
        """Click on the 'Account Information' link in the footer."""
        self.click(self.lnk_account_information)

    def click_my_account_option(self):
        """Click on the 'My Account' option in the dropdown."""
        self.click(self.dropdown)
