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
        self.lnk_my_account = page.get_by_role("link", name="My Account").first
        self.lnk_register = page.get_by_role("link", name="Register").first
        self.lnk_login = page.get_by_role("link", name="Login").first
        self.txt_search_box = page.get_by_placeholder("Search")
        self.btn_search = page.locator("#search").get_by_role("button")
        self.lnk_wishlist = page.locator("#wishlist-total")

    # ===== Action Methods =====

    def get_home_page_title(self) -> str:
        """Return the title of the Home Page."""
        self.lnk_my_account.wait_for(state="visible")
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

    def click_wishlist(self):
        """Click on the 'Wish List' link."""
        self.click(self.lnk_wishlist)

    def open_home_page(self):
        """Navigate to the home page."""
        self.open("/")

    def click_featured_product_image(self, product_name: str):
        """Click on the image of a product in the Featured section."""
        # This locator finds the product-thumb container that contains the link with the product name, then finds the image inside it.
        self.page.locator("div.product-thumb").filter(has=self.page.get_by_role("link", name=product_name, exact=True)).get_by_role("img").click()

    def click_featured_product_name(self, product_name: str):
        """Click on the name link of a product in the Featured section."""
        self.page.locator("div.product-thumb").get_by_role("link", name=product_name, exact=True).click()
