# pages/wishlist_page.py
# =====================
# Page Object for the Wishlist Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page, Locator

from pages.base_page import BasePage
from utils.constants import BreadcrumbOptionNames, ButtonNames


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
        self.alert_success = page.locator("div.alert.alert-success")

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

    def get_wishlist_table_headers(self) -> list[str]:
        """Return the wishlist table header texts."""
        return [
            header.strip() for header in self.wishlist_table.locator("thead td").all_inner_texts()
        ]

    def get_wishlist_row(self, product_name: str) -> Locator:
        """Return the wishlist row locator for a given product."""
        return self.wishlist_rows.filter(
            has=self.page.get_by_role("link", name=product_name, exact=True)
        ).first

    def get_product_image_link(self, product_name: str) -> Locator:
        """Return the product image link locator for a wishlist row."""
        return self.get_wishlist_row(product_name).locator("td").nth(0).locator("a")

    def get_product_name_link(self, product_name: str) -> Locator:
        """Return the product name link locator for a wishlist row."""
        return self.get_wishlist_row(product_name).locator("td").nth(1).get_by_role("link")

    def get_product_model(self, product_name: str) -> Locator:
        """Return the product model cell locator for a wishlist row."""
        return self.get_wishlist_row(product_name).locator("td").nth(2)

    def get_product_stock(self, product_name: str) -> Locator:
        """Return the product stock cell locator for a wishlist row."""
        return self.get_wishlist_row(product_name).locator("td").nth(3)

    def get_product_unit_price(self, product_name: str) -> Locator:
        """Return the product unit price cell locator for a wishlist row."""
        return self.get_wishlist_row(product_name).locator("td").nth(4)

    def get_add_to_cart_button(self, product_name: str) -> Locator:
        """Return the Add to Cart button locator for a wishlist row."""
        return self.get_wishlist_row(product_name).locator(
            f"button[data-original-title='{ButtonNames.ADD_TO_CART}']"
        )

    def get_remove_link(self, product_name: str) -> Locator:
        """Return the Remove action locator for a wishlist row."""
        return self.get_wishlist_row(product_name).locator(
            f"a[data-original-title='{ButtonNames.REMOVE}']"
        )

    def get_success_message(self) -> Locator:
        """Return the success message locator."""
        return self.alert_success

    def remove_product(self, product_name: str) -> "WishlistPage":
        """Remove a product from the wishlist and return self."""
        self.click(self.get_remove_link(product_name))
        return self

    def add_product_to_cart(self, product_name: str) -> "WishlistPage":
        """Add a product to the cart from the wishlist and return self."""
        self.click(self.get_add_to_cart_button(product_name))
        return self

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

    def click_product_image(self, product_name: str):
        """Click the product image link and return ProductPage instance."""
        from pages.product_page import ProductPage

        self.click(self.get_product_image_link(product_name))
        return ProductPage(self.page)

    def click_product_name(self, product_name: str):
        """Click the product name link and return ProductPage instance."""
        from pages.product_page import ProductPage

        self.click(self.get_product_name_link(product_name))
        return ProductPage(self.page)

    def click_continue_button(self):
        """Click Continue and return MyAccountPage instance."""
        from pages.my_account_page import MyAccountPage

        self.click(self.btn_continue)
        return MyAccountPage(self.page)
