# pages/product_page.py
# =====================
# Page Object for the Product Page.
# Inherits from BasePage for reusable UI interaction methods.

import re
from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.shopping_cart_page import ShoppingCartPage
from utils.constants import UITimeouts


class ProductPage(BasePage):
    """Page Object Model class for the Product Page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.content = page.locator("#content")

    # ===== Locators =====
        self.txt_quantity = self.content.locator('input[name="quantity"]')
        self.btn_add_to_cart = self.content.get_by_role("button", name="Add to Cart", exact=True)
        self.cnf_msg = page.locator("div.alert.alert-success, div.alert-success")
        self.warning_msg = page.locator("div.alert.alert-danger, div.alert-danger")
        self.any_alert_msg = page.locator("div.alert")
        self.btn_items = page.locator("#cart > button")
        self.lnk_view_cart = page.get_by_role("link", name="View Cart")

        self.btn_compare = (
            self.content
            .locator(
                'button[data-original-title="Compare this Product"], button[title="Compare this Product"]'
            )
            .first
        )
        # Link inside the success alert navigating to the product comparison page.
        self.lnk_product_comparison = self.cnf_msg.get_by_role("link", name="product comparison")
        # Link inside the success alert navigating back to the product's own display page.
        self._cnf_msg = self.cnf_msg
        self.product_header = self.content.get_by_role("heading", level=1)

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
        self.lbl_product_name = self.content.get_by_role("heading", level=1)
        self.lbl_product_brand = self.content.locator("ul.list-unstyled li", has_text="Brand:")
        self.lbl_product_code = self.content.locator("ul.list-unstyled li", has_text="Product Code:")
        self.lbl_product_availability = self.content.locator("ul.list-unstyled li", has_text="Availability:")
        self.lbl_minimum_quantity_info = page.locator(
            "#content div.alert.alert-info:has-text('minimum quantity'), #content div:has-text('minimum quantity')"
        )
        self.lnk_description_tab = self.content.locator("a[href='#tab-description'], li > a:has-text('Description')")
        self.pnl_description = self.content.locator("#tab-description")
        self.lnk_specification_tab = self.content.locator("a[href='#tab-specification']").first
        self.pnl_specification = self.content.locator("#tab-specification")
        
        # ===== Price Locators =====
        self.lbl_product_price = self.content.locator("ul.list-unstyled li h2")
        self.lbl_product_ex_tax = self.content.locator("ul.list-unstyled li", has_text="Ex Tax:")

        # ===== Thumbnail and Lightbox Locators =====
        self.thumbnail_items = self.content.get_by_role("listitem").filter(has=page.get_by_role("img"))
        self.img_main_thumbnail = self.thumbnail_items.first.get_by_role("link")
        self.lightbox = page.locator("div.mfp-container")
        self.lightbox_image = self.lightbox.get_by_role("img")
        self.btn_lightbox_next = page.get_by_title("Next (Right arrow key)")
        self.btn_lightbox_prev = page.get_by_title("Previous (Left arrow key)")
        self.btn_lightbox_close = page.get_by_title("Close (Esc)")

        # ===== Review Tab Locators =====
        self.lnk_write_review = self.content.get_by_role("link", name="Write a review")
        self.pnl_rating_summary = self.content.locator(".rating").first
        self.lbl_review_count = self.pnl_rating_summary.get_by_role("link", name=re.compile(r"^\d+\s+reviews?$", re.IGNORECASE))
        self.lnk_review_tab = self.content.get_by_role("link", name=re.compile(r"^Reviews", re.IGNORECASE))
        self.pnl_review = self.content.locator("#tab-review")

        self.txt_review_name = self.pnl_review.get_by_label("Your Name")
        self.txt_review_text = self.pnl_review.get_by_label("Your Review")
        self.btn_review_submit = self.pnl_review.get_by_role("button", name="Continue")
        self.alert_review_success = self.pnl_review.locator(".alert-success")
        self.alert_review_warning = self.pnl_review.locator(".alert-danger")
        self.lbl_no_reviews = self.pnl_review.locator("#review p")

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

    def click_specification_tab(self):
        """Click Specification tab in Product Display Page."""
        self.click(self.lnk_specification_tab.first)

    def get_specification_text(self) -> str:
        """Return product specification text from Specification tab panel."""
        text = self.pnl_specification.text_content()
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
        """Click on a normal sized Thumbnail image by its index (0-based).
        
        Since index 0 of the full list is the main thumbnail, we offset by 1.
        """
        self.click(self.thumbnail_items.nth(index + 1).get_by_role("link"))

    def get_additional_thumbnails_count(self) -> int:
        """Get the total count of additional thumbnails."""
        total = self.thumbnail_items.count()
        return max(0, total - 1)

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

    # ===== Review Tab Methods =====

    def click_write_review_link(self):
        """Click the 'Write a review' quick link on the Product Display Page."""
        self.click(self.lnk_write_review)

    def click_review_count_link(self):
        """Click the 'x reviews' link on the Product Display Page."""
        self.click(self.lbl_review_count)

    def click_review_tab(self):
        """Click the Reviews tab on the Product Display Page."""
        self.click(self.lnk_review_tab)

    def enter_review_name(self, name: str):
        """Enter the reviewer's name into the 'Your Name' field."""
        self.fill(self.txt_review_name, name)

    def enter_review_text(self, text: str):
        """Enter the review body into the 'Your Review' textarea."""
        self.fill(self.txt_review_text, text)

    def select_review_rating(self, rating_value: str):
        """Select a star rating by value (e.g. '5' for 5 stars)."""
        index = int(rating_value) - 1
        self.pnl_review.get_by_role("radio").nth(index).check()

    def submit_review(self):
        """Click the Continue button to submit the review."""
        self.click(self.btn_review_submit)

    def get_review_success_alert(self):
        """Return the review success alert locator."""
        return self.alert_review_success

    def get_review_success_text(self) -> str:
        """Return the text content of the review success alert."""
        text = self.alert_review_success.text_content()
        return text.strip() if text else ""

    def get_review_warning_alert(self):
        """Return the locator for the review validation warning."""
        return self.alert_review_warning

    def get_review_warning_text(self) -> str:
        """Return the text content of the review warning alert."""
        text = self.alert_review_warning.text_content()
        return text.strip() if text else ""

    def get_no_reviews_text(self) -> str:
        """Return the text displayed when a product has no reviews."""
        text = self.lbl_no_reviews.first.text_content()
        return text.strip() if text else ""
