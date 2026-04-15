# pages/product_page.py
# =====================
# Page Object for the Product Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.shopping_cart_page import ShoppingCartPage


class ProductPage(BasePage):
    """Page Object Model class for the Product Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.txt_quantity = page.locator('input[name="quantity"]')
        self.btn_add_to_cart = page.locator("#button-cart")
        self.cnf_msg = page.locator("div.alert.alert-success.alert-dismissible")
        self.lnk_shopping_cart_success_msg = self.cnf_msg.get_by_role(
            "link", name="shopping cart"
        )
        self.btn_items = page.locator("#cart")
        self.lnk_view_cart = page.locator('strong:has-text("View Cart")')

        self.btn_compare = (
            page.locator("#content")
            .locator(
                'button[data-original-title="Compare this Product"], button[title="Compare this Product"]'
            )
            .first
        )
        # Link inside the success alert navigating to the product comparison page.
        self.lnk_product_comparison = self.cnf_msg.get_by_role("link", name="product comparison")
        # Link inside the success alert navigating back to the product's own display page.
        self._cnf_msg = self.cnf_msg
        self.product_header = page.locator("#content").get_by_role("heading", level=1)

        # ===== Related Products Locators =====
        self.related_products_header = page.get_by_role("heading", name="Related Products")
        self.related_product_layout = page.locator(
            'h3:has-text("Related Products") ~ div .product-thumb'
        )
        self.btn_compare_related = (
            self.related_product_layout.first.get_by_role("button")
            .filter(has=page.locator(".fa-exchange"))
            .first
        )
        self.lnk_related_product_name = self.related_product_layout.first.locator("h4 a")

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

    def click_shopping_cart_in_success_message(self) -> ShoppingCartPage:
        """Click the 'shopping cart' link within the success message and return ShoppingCartPage."""
        # Wait for the success alert container first
        self.cnf_msg.wait_for(state="visible")  # no timeout needed
        # Click the 'shopping cart' link within the alert
        target_link = self.cnf_msg.get_by_role("link", name="shopping cart")
        target_link.click()
        return ShoppingCartPage(self.page)

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

    # ===== Product Verification Methods =====

    def get_product_header(self):
        """Return the product page header element (typically product name)."""
        return self.product_header

    # ===== Compare This Product Methods =====

    def get_compare_button_tooltip(self) -> str | None:
        """Return the tooltip text of the 'Compare this Product' button (data-original-title)."""
        return self.get_attribute(self.btn_compare, "data-original-title")

    def hover_compare_button(self):
        """Hover over the 'Compare this Product' button."""
        self.hover(self.btn_compare)

    def click_compare_button(self):
        """Click the 'Compare this Product' button."""
        self.click(self.btn_compare)

    def get_compare_success_message(self) -> str:
        """Return the text of the success alert shown after adding a product for comparison."""
        self.wait_for(self.cnf_msg, state="visible")
        return self.get_text(self.cnf_msg)

    def click_product_comparison_link(self):
        """Click the 'product comparison' link from the comparison success message."""
        self.click(self.lnk_product_comparison)

    def get_product_name_link_in_success_message(self, product_name: str):
        """Return the product-name link inside the comparison success alert."""
        return self._cnf_msg.get_by_role("link", name=product_name, exact=True)

    def click_product_name_link_in_success_message(self, product_name: str):
        """Click the product-name link in the comparison success alert."""
        self.click(self.get_product_name_link_in_success_message(product_name))

    # ===== Related Products Methods =====

    def get_related_product_name(self) -> str:
        """Return the name of the first related product."""
        return self.get_text(self.lnk_related_product_name)

    def hover_related_compare_button(self):
        """Hover over the 'Compare this Product' button of the first related product."""
        self.hover(self.btn_compare_related)

    def get_related_compare_button_tooltip(self) -> str | None:
        """Return the tooltip text of the related product's compare button."""
        return self.get_attribute(self.btn_compare_related, "data-original-title")

    def click_related_compare_button(self):
        """Click the 'Compare this Product' button of the first related product."""
        self.click(self.btn_compare_related)
