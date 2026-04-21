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
        self.lnk_shopping_cart_success = self.cnf_msg.get_by_role("link", name="shopping cart")
        self.warning_msg = page.locator("div.alert.alert-danger, div.alert-danger")
        self.any_alert_msg = page.locator("div.alert, .alert-success, .alert-danger, .alert-info")
        self.btn_items = page.locator("#cart > button")
        self.btn_cart_total = self.btn_items
        self.pnl_cart_dropdown = page.locator("#cart .dropdown-menu")
        self.lnk_cart_image = self.pnl_cart_dropdown.locator("table tr td.text-center a").first
        self.lnk_cart_name = self.pnl_cart_dropdown.locator("table tr td.text-left a").first
        self.lnk_view_cart = page.get_by_role("link", name="View Cart")

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
        # get_by_title
        self.btn_lightbox_close = page.get_by_title("Close (Esc)")

        # ===== Review Tab Locators =====
        # get_by_role: resolves via ARIA link role + accessible name for the quick link near the top
        self.lnk_write_review = self.content.get_by_role("link", name="Write a review")
        
        # Summary block for stars and review links above Add to Cart
        self.pnl_rating_summary = self.content.locator(".rating").first
        self.lbl_review_count = self.pnl_rating_summary.get_by_role("link", name=re.compile(r"^\d+\s+reviews?$", re.IGNORECASE))
        
        # get_by_role: Use regex to match "Reviews (0)" vs "0 reviews" (avoid strict mode violation)
        self.lnk_review_tab = self.content.get_by_role("link", name=re.compile(r"^Reviews", re.IGNORECASE))
        self.li_review_tab = self.lnk_review_tab.locator("xpath=..")
        self.pnl_review = self.content.locator("#tab-review")
        self.cnt_review = self.pnl_review.locator("#review")

        self.txt_review_name = self.pnl_review.get_by_label("Your Name")
        self.txt_review_text = self.pnl_review.get_by_label("Your Review")
        self.btn_review_submit = self.pnl_review.get_by_role("button", name="Continue")
        self.alert_review_success = self.pnl_review.locator(".alert-success")
        self.alert_review_warning = self.pnl_review.locator(".alert-danger")
        
        # Container holding actual reviews or the "no reviews" message
        self.lbl_no_reviews = self.pnl_review.locator("#review p")

        # ===== Social and Utility Locators =====
        self.btn_wishlist = page.locator("button").filter(has=page.locator("i.fa-heart")).first
        self.btn_compare = page.locator("button").filter(has=page.locator("i.fa-exchange")).first
        self.pnl_social_sharing = page.locator(".addthis_sharing_toolbox, .addthis_inline_share_toolbox")
        self.btn_facebook_like = page.locator(".addthis_button_facebook_like")
        
        self.pnl_related_products = self.content.get_by_role("heading", name="Related Products")
        self.lnk_related_product = page.locator(".product-thumb h4 a")

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

    def get_any_alert_message(self):
        """Return the first alert/success message locator found on the page."""
        return self.any_alert_msg.first

    # ===== Navigate to Shopping Cart =====

    def click_items_to_navigate_to_cart(self):
        """Click the cart icon to open the cart dropdown."""
        self.click(self.btn_items)

    def click_view_cart(self) -> ShoppingCartPage:
        """Click 'View Cart' link and return ShoppingCartPage instance."""
        self.click(self.lnk_view_cart)
        return ShoppingCartPage(self.page)

    def click_shopping_cart_link(self) -> ShoppingCartPage:
        """Click the 'shopping cart' link from the success message."""
        self.click(self.lnk_shopping_cart_success)
        return ShoppingCartPage(self.page)

    def click_wishlist_link_on_success_msg(self):
        """Click the 'wish list' link within any visible alert message."""
        # This uses self.any_alert_msg from locators to find the embedded link
        self.any_alert_msg.first.get_by_role("link", name=re.compile(r"wish list", re.IGNORECASE)).click()

    def click_comparison_link_on_success_msg(self):
        """Click the 'product comparison' link within any visible alert message."""
        self.any_alert_msg.first.get_by_role("link", name=re.compile(r"product comparison", re.IGNORECASE)).click()

    # ===== Cart Toggle Box Methods =====

    def click_cart_button(self):
        """Click the cart button to open the toggle box."""
        self.click(self.btn_cart_total)

    def click_cart_image_link(self) -> "ProductPage":
        """Click the product image in the cart toggle box and return ProductPage."""
        from pages.product_page import ProductPage
        self.click(self.lnk_cart_image)
        return ProductPage(self.page)

    def click_cart_name_link(self) -> "ProductPage":
        """Click the product name link in the cart toggle box and return ProductPage."""
        from pages.product_page import ProductPage
        self.click(self.lnk_cart_name)
        return ProductPage(self.page)

    # ===== Combined Workflow =====

    def add_product_to_cart(self, quantity: str):
        """Set quantity, add to cart, and verify confirmation message."""
        self.set_quantity(quantity)
        self.add_to_cart()
        expect(self.get_confirmation_message()).to_be_visible()

    # ===== Product Details Methods =====

    def get_product_name(self) -> str:
        """Return the product name."""
        return self.get_text(self.lbl_product_name).strip() if self.lbl_product_name.is_visible() else ""

    def get_product_brand(self) -> str:
        """Return the product brand."""
        text = self.get_text(self.lbl_product_brand)
        return text.replace("Brand:", "").strip() if text else ""

    def get_product_code(self) -> str:
        """Return the product code."""
        text = self.get_text(self.lbl_product_code)
        return text.replace("Product Code:", "").strip() if text else ""

    def get_product_availability(self) -> str:
        """Return the product availability status."""
        text = self.get_text(self.lbl_product_availability)
        return text.replace("Availability:", "").strip() if text else ""

    def get_default_quantity_value(self) -> str:
        """Return quantity textbox current value."""
        return self.get_element_attribute(self.txt_quantity, "value") or ""

    def get_minimum_quantity_info_text(self) -> str:
        """Return minimum quantity helper/info text from PDP."""
        text = self.get_text(self.lbl_minimum_quantity_info.first)
        return text.strip() if text else ""

    def click_description_tab(self):
        """Click Description tab in Product Display Page."""
        self.click(self.lnk_description_tab.first)

    def get_description_text(self) -> str:
        """Return product description text from Description tab panel."""
        text = self.get_text(self.pnl_description)
        return text.strip() if text else ""

    def click_specification_tab(self):
        """Click Specification tab in Product Display Page."""
        self.click(self.lnk_specification_tab.first)

    def get_specification_text(self) -> str:
        """Return product specification text from Specification tab panel."""
        text = self.get_text(self.pnl_specification)
        return text.strip() if text else ""

    # ===== Price Methods =====

    def get_product_price(self) -> str:
        """Return the main product price."""
        return self.get_text(self.lbl_product_price).strip() if self.lbl_product_price.is_visible() else ""

    def get_ex_tax_price(self) -> str:
        """Return the ex-tax price text."""
        text = self.get_text(self.lbl_product_ex_tax)
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
        """Select a star rating by value (e.g. '5' for 5 stars).

        Since OpenCart rating radios lack standard <label> wrappers, 
        we compute the 0-based index from the 1-5 rating value safely 
        using pure role locators.
        """
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
        text = self.get_text(self.alert_review_success)
        return text.strip() if text else ""

    def get_review_warning_alert(self):
        """Return the locator for the review validation warning."""
        return self.alert_review_warning

    def get_review_warning_text(self) -> str:
        """Return the text content of the review warning alert."""
        text = self.get_text(self.alert_review_warning)
        return text.strip() if text else ""

    def get_no_reviews_text(self) -> str:
        """Return the text displayed when a product has no reviews."""
        text = self.get_text(self.lbl_no_reviews.first)
        return text.strip() if text else ""

    # ===== Wishlist and Comparison Methods =====

    def click_add_to_wishlist(self):
        """Click the 'Add to Wish List' button."""
        self.click(self.btn_wishlist)

    def click_compare(self):
        """Click the 'Compare' button."""
        self.click(self.btn_compare)

    def get_social_sharing_widget(self):
        """Return the locator for the AddThis social sharing widget."""
        return self.pnl_social_sharing

    def get_facebook_like_button(self):
        """Return the locator for the Facebook Like button."""
        return self.btn_facebook_like

    # ===== Social and Related Products Methods =====

    def click_related_product(self, index: int):
        """Click the n-th related product."""
        self.click(self.lnk_related_product.nth(index))

    def get_related_products_count(self) -> int:
        """Get the total count of related products."""
        return self.lnk_related_product.count()

    def scroll_to_related_products(self):
        """Scroll the related products section into view."""
        self.pnl_related_products.scroll_into_view_if_needed()

    def get_related_product_name(self, index: int) -> str:
        """Return the name of the n-th related product."""
        return self.get_text(self.lnk_related_product.nth(index)).strip()
