# pages/home_page.py

from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.contact_us_page import ContactUsPage
from pages.login_page import LoginPage


class HomePage(BasePage):
    """Page Object Model class for the Home page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.icon_phone_contact = page.locator("ul.list-inline li a:has(i.fa-phone)")
        self.footer_lnk_contact_us = page.locator("footer").get_by_role("link", name="Contact Us")
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

    # ===== Header Contact Us Link =====

    def verify_contact_us_link_visible(self):
        """Verify the Contact Us link is visible in the header."""
        assert self.is_visible(self.lnk_contact_us)

    def click_contact_us(self):
        """Click on the Contact Us link."""
        self.click(self.lnk_contact_us)
        return ContactUsPage(self.page)

    def navigate_to_contact_us_page(self):
        """Navigate to the Contact Us page."""
        self.verify_contact_us_link_visible()
        return self.click_contact_us()

    # ===== Header Phone Icon =====

    def verify_phone_icon_visible(self):
        assert self.is_visible(self.icon_phone_contact)

    def click_phone_icon_contact(self):
        self.click(self.icon_phone_contact)
        return ContactUsPage(self.page)

    def navigate_to_contact_us_from_phone_icon(self):
        self.verify_phone_icon_visible()
        return self.click_phone_icon_contact()

    # ===== Footer Contact Us =====

    def verify_footer_contact_us_link_visible(self):
        assert self.is_visible(self.footer_lnk_contact_us)

    def click_footer_contact_us(self):
        self.click(self.footer_lnk_contact_us)
        return ContactUsPage(self.page)

    def navigate_to_contact_us_from_footer(self):
        self.verify_footer_contact_us_link_visible()
        return self.click_footer_contact_us()

    # ===== Other Methods =====

    def click_desktops_category(self):
        self.click(self.lnk_desktops)

    def logout_link(self):
        """Click on the 'Logout' link."""
        return self.lnk_logout

    def is_dropdown_menu_visible(self) -> bool:
        """Return True if the dropdown menu is visible."""
        return self.is_visible(self.dropdown)

    def click_show_all_desktops(self):
        self.click(self.lnk_show_all_desktops)
