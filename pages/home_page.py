# pages/home_page.py
# =====================
# Page Object for the Home Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page

from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object Model class for the Home page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.lnk_my_account = page.locator('span:has-text("My Account")')
        self.lnk_register = page.locator('a:has-text("Register")')
        self.lnk_login = page.locator('a:has-text("Login")')
        self.txt_search_box = page.locator('input[placeholder="Search"]')
        self.btn_search = page.locator('#search button[type="button"]')

    # ===== Action Methods =====

    def get_home_page_title(self) -> str:
        """Return the title of the Home Page."""
        self.lnk_my_account.wait_for(state="visible")
        return self.get_title()

    def click_my_account(self):
        """Click on the 'My Account' link."""
        self.lnk_my_account.click()

    def click_register(self):
        """Click on the 'Register' link under My Account."""
        self.lnk_register.click()

    def click_login(self):
        """Click on the 'Login' link under My Account."""
        self.lnk_login.click()

    def enter_product_name(self, product_name: str):
        """Enter the product name into the search input box."""
        self.txt_search_box.fill(product_name)

    def click_search(self):
        """Click on the search button to initiate the product search."""
        self.btn_search.click()

    def open_home_page(self):
        self.page.goto("/")
        # self.page.wait_for_load_state("networkidle")
