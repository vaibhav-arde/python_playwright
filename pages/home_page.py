# pages/home_page.py
# =====================
# Page Object for the Home Page.
# Inherits from BasePage for reusable UI interaction methods.

import re

from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.category_page import CategoryPage
from pages.login_page import LoginPage
from pages.wishlist_page import WishlistPage
from utils.constants import FooterOptionNames


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
        self.lnk_logout = page.locator('a:has-text("Logout")')
        self.lnk_contact_us = page.get_by_role("link", name="Contact Us")
        self.lnk_desktops = page.get_by_role("link", name="Desktops")
        self.lnk_show_all_desktops = page.get_by_role("link", name="Show AllDesktops")
        self.dropdown = page.locator("a.dropdown-toggle").filter(has_text="My Account")
        self.lnk_change_password = page.get_by_role("link", name="Change your password")

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
        self.lnk_logo = page.locator("#logo a")
        self.featured_section = page.locator("h3:has-text('Featured')")
        self.success_msg = page.locator(".alert-success")
        self.lnk_wishlist_success = self.success_msg.get_by_role("link", name="wish list")
        self.lnk_wishlist_footer = page.locator("footer").get_by_role(
            "link", name=FooterOptionNames.WISH_LIST, exact=True
        )

    # ===== Action Methods =====

    def get_home_page_title(self) -> str:
        """Return the title of the Home Page."""
        return self.get_title()

    def click_my_account(self):
        """Click on the 'My Account' link."""
        self.click(self.lnk_my_account)

    def click_change_password(self):
        """Click on the 'Change your password' link."""
        self.click(self.lnk_change_password)

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

    def click_wishlist_footer_option(self):
        """Click the footer 'Wish List' link."""
        self.click(self.lnk_wishlist_footer)
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
