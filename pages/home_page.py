# pages/home_page.py
# =====================
# Page Object for the Home Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page, Locator

from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object Model class for the Home page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.lnk_my_account = page.locator('span:has-text("My Account")')
        self.lnk_register = page.locator('a:has-text("Register")')
        self.lnk_login = page.locator("ul.dropdown-menu").get_by_role("link", name="Login")
        self.lnk_logout = page.locator("ul.dropdown-menu").get_by_role("link", name="Logout")
        self.dropdown_menu = page.locator("ul.dropdown-menu").filter(has_text="Logout").first
        self.my_account_inner_link = self.dropdown_menu.get_by_role("link", name="My Account")
        self.txt_search_box = page.locator('input[placeholder="Search"]')
        self.btn_search = page.locator('#search button[type="button"]')

    # ===== Action Methods =====

    def get_dropdown_menu(self) -> Locator:
        """Return the dropdown menu container."""
        return self.dropdown_menu

    def get_my_account_inner_link(self) -> Locator:
        """Return the 'My Account' link inside the dropdown."""
        return self.my_account_inner_link

    def get_expected_title(self) -> str:
        """Return the expected title for the Home Page."""
        # Opencart Default
        return "Your Store"

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

    def verify_login_btn_visible(self):
        return self.lnk_login
        
    def verify_logout_btn_not_visible(self):
        return self.lnk_logout