# pages/product_page.py
# =====================
# Page Object for the Product Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.shopping_cart_page import ShoppingCartPage
from pages.wishlist_page import WishlistPage


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

        # Related Products
        self.related_products_section = page.locator(".product-thumb")
        self.wishlist_link_in_msg = self.cnf_msg.get_by_role("link", name="wish list")

    # ===== Quantity Methods =====

    def set_quantity(self, qty: str):
        """Set the desired product quantity."""
        self.fill(self.txt_quantity, "")
        self.fill(self.txt_quantity, qty)

    # ===== Add to Cart Methods =====

    def add_to_cart(self):
        """Click the 'Add to Cart' button."""
        self.click(self.btn_add_to_cart)

    # ===== Confirmation Message =====

    def get_confirmation_message(self):
        """Return the confirmation message element shown after adding to cart."""
        return self.cnf_msg

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

    def add_related_product_to_wishlist(self, index: int = 0) -> str:
        """
        Click 'Add to Wish List' on a related product by index.
        Returns the name of the product that was added.
        """
        product = self.related_products_section.nth(index)
        product_name = product.locator("h4 a").text_content()
        # Find the wishlist button for this specific related product
        wishlist_btn = product.get_by_role("button", name="Add to Wish List", exact=False).or_(
            product.locator("button[data-original-title='Add to Wish List']")
        )
        self.click(wishlist_btn)
        return product_name.strip() if product_name else ""

    def click_wishlist_link_in_message(self) -> WishlistPage:
        """Click the 'wish list!' link in the success message."""
        self.click(self.wishlist_link_in_msg)
        return WishlistPage(self.page)
