# pages/product_page.py
# =====================
# Page Object for the Product Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.shopping_cart_page import ShoppingCartPage
from utils.constants import UITimeouts


class ProductPage(BasePage):
    """Page Object Model class for the Product Page."""

    def __init__(self, page: Page):
        super().__init__(page)

    # ===== Locators =====
        self.txt_quantity = page.locator('input[name="quantity"]')
        self.btn_add_to_cart = page.locator("#button-cart")
        self.cnf_msg = page.locator("div.alert.alert-success.alert-dismissible")
        self.warning_msg = page.locator("div.alert.alert-danger.alert-dismissible, div.alert.alert-danger")
        self.any_alert_msg = page.locator("div.alert")
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

        # ===== Product Details Locators =====
        self.lbl_product_name = page.locator("#content h1")
        self.lbl_product_brand = page.locator("ul.list-unstyled >> li:has-text('Brand:')")
        self.lbl_product_code = page.locator("ul.list-unstyled >> li:has-text('Product Code:')")
        self.lbl_product_availability = page.locator("ul.list-unstyled >> li:has-text('Availability:')")
        self.lbl_minimum_quantity_info = page.locator(
            "#content div.alert.alert-info:has-text('minimum quantity'), #content div:has-text('minimum quantity')"
        )
        self.lnk_description_tab = page.locator("a[href='#tab-description'], a:has-text('Description')")
        self.pnl_description = page.locator("#tab-description")
        
        # ===== Price Locators =====
        self.lbl_product_price = page.locator("#content ul.list-unstyled li h2")
        self.lbl_product_ex_tax = page.locator("#content ul.list-unstyled li:has-text('Ex Tax:')")

        # ===== Thumbnail and Lightbox Locators =====
        self.img_main_thumbnail = page.locator("ul.thumbnails > li:nth-child(1) > a.thumbnail")
        self.img_additional_thumbnails = page.locator("ul.thumbnails > li.image-additional > a.thumbnail")
        self.lightbox = page.locator("div.mfp-container") # Magnific popup container is usually the direct parent handling visibility/clicks
        self.lightbox_image = page.locator("img.mfp-img")
        self.btn_lightbox_next = page.locator("button.mfp-arrow-right")
        self.btn_lightbox_prev = page.locator("button.mfp-arrow-left")
        self.btn_lightbox_close = page.locator("button.mfp-close")

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

    def get_warning_message(self):
        """Return the warning message element shown after add-to-cart validation."""
        return self.warning_msg

    def wait_for_cart_feedback(self, timeout: int = UITimeouts.CART_ALERT_WAIT_MS):
        """Wait until any cart feedback alert (success/warning) is displayed."""
        self.any_alert_msg.first.wait_for(state="visible", timeout=timeout)

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

    # ===== Product Details Methods =====

    def get_product_name(self) -> str:
        """Return the product name."""
        return self.lbl_product_name.text_content().strip() if self.lbl_product_name.is_visible() else ""

    def get_product_brand(self) -> str:
        """Return the product brand."""
        text = self.lbl_product_brand.text_content()
        return text.replace("Brand:", "").strip() if text else ""

    def get_product_code(self) -> str:
        """Return the product code."""
        text = self.lbl_product_code.text_content()
        return text.replace("Product Code:", "").strip() if text else ""

    def get_product_availability(self) -> str:
        """Return the product availability status."""
        text = self.lbl_product_availability.text_content()
        return text.replace("Availability:", "").strip() if text else ""

    def get_default_quantity_value(self) -> str:
        """Return quantity textbox current value."""
        return self.get_attribute(self.txt_quantity, "value") or ""

    def get_minimum_quantity_info_text(self) -> str:
        """Return minimum quantity helper/info text from PDP."""
        text = self.lbl_minimum_quantity_info.first.text_content()
        return text.strip() if text else ""

    def click_description_tab(self):
        """Click Description tab in Product Display Page."""
        self.click(self.lnk_description_tab.first)

    def get_description_text(self) -> str:
        """Return product description text from Description tab panel."""
        text = self.pnl_description.text_content()
        return text.strip() if text else ""

    # ===== Price Methods =====

    def get_product_price(self) -> str:
        """Return the main product price."""
        return self.lbl_product_price.text_content().strip() if self.lbl_product_price.is_visible() else ""

    def get_ex_tax_price(self) -> str:
        """Return the ex-tax price text."""
        text = self.lbl_product_ex_tax.text_content()
        return text.replace("Ex Tax:", "").strip() if text else ""

    # ===== Thumbnail and Lightbox Methods =====

    def click_main_thumbnail(self):
        """Click on the main bigger sized Thumbnail image."""
        self.click(self.img_main_thumbnail)

    def click_additional_thumbnail(self, index: int):
        """Click on a normal sized Thumbnail image by its index."""
        self.click(self.img_additional_thumbnails.nth(index))

    def get_additional_thumbnails_count(self) -> int:
        """Get the total count of additional thumbnails."""
        return self.img_additional_thumbnails.count()

    def get_lightbox(self):
        """Return the Lightbox container locator."""
        return self.lightbox

    def get_lightbox_image(self):
        """Return the Lightbox image locator."""
        return self.lightbox_image

    def click_lightbox_next(self):
        """Click the '>' (next) option in Lightbox."""
        self.click(self.btn_lightbox_next)

    def click_lightbox_prev(self):
        """Click the '<' (prev) option in Lightbox."""
        self.click(self.btn_lightbox_prev)

    def click_lightbox_close(self):
        """Click the 'x' (close) option in Lightbox."""
        self.click(self.btn_lightbox_close)

    def press_escape_key(self):
        """Press the 'ESC' keyboard key."""
        self.page.keyboard.press("Escape")
