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
        self.lnk_my_account = page.get_by_role("link", name="My Account").first
        self.lnk_register = page.get_by_role("link", name="Register").first
        self.lnk_login = page.get_by_role("link", name="Login").first
        self.txt_search_box = page.get_by_placeholder("Search")
        self.btn_search = page.locator("#search").get_by_role("button")
        self.lnk_logout = page.locator('a:has-text("Logout")')
        self.lnk_contact_us = page.get_by_role("link", name="Contact Us")
        self.lnk_desktops = page.get_by_role("link", name="Desktops")
        self.lnk_show_all_desktops = page.get_by_role("link", name="Show AllDesktops")
        self.dropdown = page.locator("a.dropdown-toggle").filter(has_text="My Account")
        self.lnk_wishlist = page.locator("#wishlist-total")
        self.lnk_shopping_cart = page.get_by_role("link", name="Shopping Cart").first
        self.btn_cart_total = page.locator("#cart > button")
        self.lnk_view_cart = page.get_by_role("link", name="View Cart")

    # ===== Action Methods =====

    def get_home_page_title(self) -> str:
        """Return the title of the Home Page."""
        self.lnk_my_account.wait_for(state="visible")
        return self.get_title()

    def click_my_account(self):
        """Click on the 'My Account' link."""
        self.lnk_my_account.wait_for(state="visible")
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

    def click_wishlist(self):
        """Click on the 'Wish List' link."""
        self.click(self.lnk_wishlist)

    def click_shopping_cart(self):
        """Click on the 'Shopping Cart' link in the top bar."""
        self.click(self.lnk_shopping_cart)

    def click_cart_total_button(self):
        """Click the black cart button to open the dropdown."""
        self.click(self.btn_cart_total)

    def click_view_cart(self):
        """Click 'View Cart' link from the cart dropdown."""
        self.click(self.lnk_view_cart)

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
