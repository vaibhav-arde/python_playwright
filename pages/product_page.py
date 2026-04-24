# pages/product_page.py
# =====================
# Page Object for the Product Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.shopping_cart_page import ShoppingCartPage
from pages.wishlist_page import WishlistPage
from utils.constants import (
    ButtonNames,
    CommonValues,
    HeaderOptionNames,
    ProductDetailLabels,
)


class ProductPage(BasePage):
    """Page Object Model class for the Product Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.txt_quantity = page.locator('input[name="quantity"]')
        self.btn_add_to_cart = page.locator("#button-cart")
        self.cnf_msg = page.locator("div.alert.alert-success.alert-dismissible")
        self.btn_items = page.locator("#cart")
        self.lnk_view_cart = page.locator('strong:has-text("View Cart")')
        self.btn_add_to_wishlist = page.locator(
            f"button[data-original-title='{ButtonNames.ADD_TO_WISH_LIST}']"
        ).first
        self.msg_product_page_heading = page.locator("#content h1")
        self.product_details_section = page.locator("#content .col-sm-4").first
        self.txt_product_code = (
            self.product_details_section.locator("ul.list-unstyled")
            .nth(0)
            .locator("li")
            .filter(has_text=ProductDetailLabels.PRODUCT_CODE)
            .first
        )
        self.txt_availability = (
            self.product_details_section.locator("ul.list-unstyled")
            .nth(0)
            .locator("li")
            .filter(has_text=ProductDetailLabels.AVAILABILITY)
            .first
        )
        self.txt_unit_price = (
            self.product_details_section.locator("ul.list-unstyled").nth(1).locator("h2")
        )
        self.lnk_wishlist_header = page.locator("#top-links").get_by_role(
            "link", name=HeaderOptionNames.WISH_LIST, exact=False
        )

        # Related Products
        self.related_products_section = page.locator(".product-thumb")
        self.wishlist_link_in_msg = self.cnf_msg.get_by_role("link", name="wish list")

    # ===== Quantity Methods =====

    def set_quantity(self, qty: str):
        """Set the desired product quantity."""
        self.fill(self.txt_quantity, CommonValues.EMPTY)
        self.fill(self.txt_quantity, qty)

    # ===== Add to Cart Methods =====

    def add_to_cart(self):
        """Click the 'Add to Cart' button."""
        self.click(self.btn_add_to_cart)

    # ===== Confirmation Message =====

    def get_confirmation_message(self):
        """Return the confirmation message element shown after adding to cart."""
        return self.cnf_msg

    def get_product_page_heading(self):
        """Return the product display page heading locator."""
        return self.msg_product_page_heading

    def get_product_model_value(self) -> str:
        """Return the product code value displayed on the product page."""
        return self.get_text(self.txt_product_code).split(":", 1)[1].strip()

    def get_product_stock_value(self) -> str:
        """Return the availability value displayed on the product page."""
        return self.get_text(self.txt_availability).split(":", 1)[1].strip()

    def get_product_unit_price_value(self) -> str:
        """Return the unit price displayed on the product page."""
        return self.get_text(self.txt_unit_price).strip()

    # ===== Navigate to Shopping Cart =====

    def click_items_to_navigate_to_cart(self):
        """Click the cart icon to open the cart dropdown."""
        self.click(self.btn_items)

    def click_view_cart(self) -> ShoppingCartPage:
        """Click 'View Cart' link and return ShoppingCartPage instance."""
        self.click(self.lnk_view_cart)
        return ShoppingCartPage(self.page)

    # ===== Combined Workflow =====

    def add_product_to_cart(self, quantity: str):
        """Set quantity, add to cart, and verify confirmation message."""
        self.set_quantity(quantity)
        self.add_to_cart()
        expect(self.get_confirmation_message()).to_be_visible()

    # ===== Wishlist Methods =====

    def add_product_to_wishlist(self) -> None:
        """Click 'Add to Wish List' on the displayed product."""
        self.click(self.btn_add_to_wishlist)

    def add_related_product_to_wishlist(self, index: int = 0) -> str:
        """
        Click 'Add to Wish List' on a related product by index.
        Returns the name of the product that was added.
        """
        product = self.related_products_section.nth(index)
        product_name = product.locator("h4 a").text_content()
        # Find the wishlist button for this specific related product
        wishlist_btn = product.get_by_role(
            "button", name=ButtonNames.ADD_TO_WISH_LIST, exact=False
        ).or_(product.locator(f"button[data-original-title='{ButtonNames.ADD_TO_WISH_LIST}']"))
        self.click(wishlist_btn)
        return product_name.strip() if product_name else CommonValues.EMPTY

    def click_wishlist_link_in_message(self) -> WishlistPage:
        """Click the 'wish list!' link in the success message."""
        self.click(self.wishlist_link_in_msg)
        return WishlistPage(self.page)

    def click_wishlist_header_option(self) -> WishlistPage:
        """Click the header 'Wish List' option."""
        self.click(self.lnk_wishlist_header)
        return WishlistPage(self.page)
