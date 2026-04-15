# pages/home_page.py
# =====================
# Page Object for the Home Page.
# Inherits from BasePage for reusable UI interaction methods.

import re

from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.search_results_page import SearchResultsPage


class HomePage(BasePage):
    """Page Object Model class for the Home page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        # This is the dropdown toggle that opens the account menu.
        self.lnk_my_account = page.locator('#top-links a[title="My Account"]')
        self.lnk_register = page.locator(
            "#top-links ul.dropdown-menu.dropdown-menu-right"
        ).get_by_text("Register", exact=True)
        self.lnk_login = page.locator(
            "#top-links ul.dropdown-menu.dropdown-menu-right"
        ).get_by_text("Login", exact=True)
        self.lnk_desktops_menu = page.get_by_role("link", name="Desktops", exact=True)
        # The menu renders as "Show AllDesktops" in the DOM, so a regex keeps this semantic.
        self.lnk_show_all_desktops = page.get_by_role(
            "link", name=re.compile(r"Show All\s*Desktops")
        )
        self.txt_search_box = page.locator('input[placeholder="Search"]')
        self.btn_search = page.locator('#search button[type="button"]')
        self.img_logo = page.locator("#logo a")  # ✅ Added logo locator

        # ===== Featured Section Locators =====
        self.featured_products_section = page.locator(
            'h3:has-text("Featured") ~ .row .product-thumb'
        )
        self.btn_compare_featured = (
            self.featured_products_section.first.get_by_role("button")
            .filter(has=page.locator(".fa-exchange"))
            .first
        )
        self.lnk_featured_product_name = self.featured_products_section.first.locator("h4 a")
        self.compare_success_message = page.locator("div.alert.alert-success.alert-dismissible")
        self.lnk_product_comparison = self.compare_success_message.get_by_role(
            "link", name="product comparison"
        )

    # ===== Action Methods =====

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

    def get_desktops_menu(self):
        """Return the 'Desktops' menu locator."""
        return self.lnk_desktops_menu

    def hover_desktops_menu(self):
        """Hover over the 'Desktops' top menu."""
        self.hover(self.lnk_desktops_menu)

    def get_show_all_desktops_link(self):
        """Return the 'Show All Desktops' menu link locator."""
        return self.lnk_show_all_desktops

    def click_show_all_desktops(self):
        """Click on the 'Show All Desktops' option under Desktops."""
        self.click(self.lnk_show_all_desktops)

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

    # ===== Featured Section Methods =====

    def get_first_featured_product_name(self) -> str:
        """Return the name of the first product in the Featured section."""
        return self.get_text(self.lnk_featured_product_name)

    def hover_featured_compare_button(self):
        """Hover over the 'Compare this Product' button of the first featured product."""
        self.hover(self.btn_compare_featured)

    def get_featured_compare_button_tooltip(self) -> str | None:
        """Return the tooltip text (title) of the featured product's compare button."""
        return self.get_attribute(self.btn_compare_featured, "data-original-title")

    def click_featured_compare_button(self):
        """Click the 'Compare this Product' button of the first featured product."""
        self.click(self.btn_compare_featured)

    def get_compare_success_message(self) -> str:
        """Return the success message shown after adding a product for comparison."""
        self.wait_for(self.compare_success_message, state="visible")
        return self.get_text(self.compare_success_message)

    def click_product_comparison_link(self):
        """Click the 'product comparison' link from the success message."""
        self.click(self.lnk_product_comparison)
        return SearchResultsPage(self.page)

    def click_logo(self):
        """Clicks on the site logo and returns HomePage"""
        self.click(self.img_logo)
        return HomePage(self.page)
