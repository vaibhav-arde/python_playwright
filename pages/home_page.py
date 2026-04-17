# pages/home_page.py
# =====================
# Page Object for the Home Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.search_results_page import SearchResultsPage


class HomePage(BasePage):
    """Page Object Model class for the Home page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ==================================================
        # Header Locators
        # ==================================================
        self.lnk_my_account = page.locator('span:has-text("My Account")')
        self.lnk_register = page.locator('a:has-text("Register")')
        self.lnk_login = page.locator(
            "ul.dropdown-menu"
        ).get_by_role("link", name="Login")
        self.txt_search_box = page.locator('input[placeholder="Search"]')
        self.btn_search = page.locator('#search button[type="button"]')
        self.img_logo = page.locator("#logo a")
        self.main_menu = page.locator("#menu")
        self.footer = page.locator("footer")

        # ==================================================
        # Category Navigation
        # ==================================================
        self.lnk_desktops = page.locator(
            '#menu .nav > li > a:has-text("Desktops")'
        )
        self.lnk_pc = page.get_by_role(
            "link",
            name="PC (0)",
            exact=True
        )

        # ==================================================
        # Hero Slider Locators
        # ==================================================
        self.cnt_hero_slider = page.locator("#slideshow0")
        self.btn_slider_next = self.cnt_hero_slider.locator(
            ".swiper-button-next"
        )
        self.btn_slider_prev = self.cnt_hero_slider.locator(
            ".swiper-button-prev"
        )
        self.list_slider_images = self.cnt_hero_slider.locator(
            ".swiper-slide img"
        )
        self.list_slider_pagination = page.locator(
            ".swiper-pagination-bullet"
        )
        self.img_active_hero = self.cnt_hero_slider.locator(
            ".swiper-slide-active img, "
            ".swiper-slide-duplicate-active img"
        ).first

        # ==================================================
        # Featured Products Locators
        # ==================================================
        self.txt_featured_heading = page.locator(
            'h3:has-text("Featured")'
        )
        self.list_featured_products = page.locator(
            "#content .product-layout"
        )

        # ==================================================
        # Partner Carousel Locators
        # ==================================================
        self.partner_carousel = page.locator("#carousel0")
        self.partner_slides = self.partner_carousel.locator(
            ".swiper-slide"
        )
        self.active_partner = self.partner_carousel.locator(
            ".swiper-slide-active"
        )
        self.next_partner = self.partner_carousel.locator(
            ".swiper-slide-next"
        )
        self.prev_partner = self.partner_carousel.locator(
            ".swiper-slide-prev"
        )
        self.partner_wrapper = self.partner_carousel.locator(
            ".swiper-wrapper"
        )
        self.btn_partner_next = self.partner_carousel.locator(
            ".swiper-button-next"
        )
        self.btn_partner_prev = self.partner_carousel.locator(
            ".swiper-button-prev"
        )
        self.partner_pagination = page.locator(
            ".swiper-pagination-bullet"
        )

        # ==================================================
        # Breadcrumb Locators
        # ==================================================
        self.icon_breadcrumb_home = page.locator(
            "ul.breadcrumb li:first-child a"
        )

    # ==================================================
    # Common Actions
    # ==================================================

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

    def click_logo(self):
        """Click on the site logo."""
        self.click(self.img_logo)
        return self

    def verify_logo_visible(self):
        """Verify logo is visible."""
        expect(self.img_logo).to_be_visible()

    def verify_search_bar_visible(self):
        """Verify search bar is visible."""
        expect(self.txt_search_box).to_be_visible()

    def verify_main_menu_visible(self):
        """Verify main menu is visible."""
        expect(self.main_menu).to_be_visible()

    def verify_footer_visible(self):
        """Verify footer is visible."""
        expect(self.footer).to_be_visible()

    # ==================================================
    # Search Methods
    # ==================================================

    def enter_product_name(self, product_name: str):
        """Enter product name."""
        self.fill(self.txt_search_box, product_name)

    def click_search(self):
        """Click Search."""
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

    # ==================================================
    # Category Navigation
    # ==================================================

    def navigate_to_empty_pc_category(self):
        """Hover Desktops and click PC(0)."""
        self.lnk_desktops.hover()
        self.lnk_pc.click()

    # ==================================================
    # Hero Slider Methods
    # ==================================================

    def verify_slider_is_visible(self):
        """Verify hero slider visible."""
        expect(self.cnt_hero_slider).to_be_visible()

    def get_slider_images_count(self) -> int:
        """Return total hero images."""
        self.list_slider_images.first.wait_for(
            state="visible"
        )
        return self.list_slider_images.count()

    def verify_slider_images_present(self):
        """Verify at least one hero image is present."""
        count = self.get_slider_images_count()

        assert count > 0, (
            f"Expected hero images > 0, but got {count}"
        )

    def verify_navigation_buttons_are_visible(self):
        """Verify Next / Prev buttons visible if present."""
        if self.btn_slider_next.count() > 0:
            expect(self.btn_slider_next).to_be_visible()

        if self.btn_slider_prev.count() > 0:
            expect(self.btn_slider_prev).to_be_visible()

    def click_slider_next(self):
        """Click Next arrow if present."""
        if self.btn_slider_next.count() > 0:
            self.btn_slider_next.click()

    def click_slider_prev(self):
        """Click Previous arrow if present."""
        if self.btn_slider_prev.count() > 0:
            self.btn_slider_prev.click()

    def get_active_image_src(self) -> str:
        """Return active image src."""
        src = self.img_active_hero.get_attribute("src")
        return src if src else ""

    def verify_image_changed(self, previous_src: str):
        """Verify image changed after slider transition."""
        max_attempts = 10
        new_src = previous_src

        for _ in range(max_attempts):
            self.page.wait_for_timeout(300)
            new_src = self.get_active_image_src()

            if new_src != previous_src:
                break

        assert new_src != previous_src, (
            f"Expected image to change. "
            f"Old: {previous_src}, "
            f"New: {new_src}"
        )

    def verify_pagination_is_visible(self):
        """Verify pagination dots visible."""
        expect(
            self.list_slider_pagination.first
        ).to_be_visible()

    # ==================================================
    # Featured Products Methods
    # ==================================================

    def verify_featured_section_visible(self):
        """Verify Featured heading is visible."""
        expect(
            self.txt_featured_heading
        ).to_be_visible()

    def get_featured_products_count(self) -> int:
        """Return featured products count."""
        return self.list_featured_products.count()

    def verify_four_featured_products(self):
        """Verify exactly four featured products displayed."""
        count = self.get_featured_products_count()

        assert count == 4, (
            f"Expected 4 featured products, "
            f"but got {count}"
        )

    # ==================================================
    # Partner Carousel Methods
    # ==================================================

    def verify_partner_carousel_visible(self):
        """Verify Partner Carousel is visible."""
        expect(self.partner_carousel).to_be_visible()

    def verify_partner_logos_visible(self):
        """Verify Partner logos are visible."""
        expect(
            self.partner_slides.first
        ).to_be_visible()

    def get_partner_logos_count(self) -> int:
        """Return Partner logos count."""
        return self.partner_slides.count()

    def verify_multiple_partner_logos(self):
        """Verify multiple Partner logos displayed."""
        count = self.get_partner_logos_count()

        assert count >= 5, (
            f"Expected at least 5 partner logos, "
            f"but got {count}"
        )

    def get_active_partner_index(self) -> str:
        """Return active partner slide index."""
        index = self.active_partner.get_attribute(
            "data-swiper-slide-index"
        )
        return index if index else ""

    def verify_partner_navigation_buttons_visible(self):
        """Verify Partner slider arrows visible."""
        if self.btn_partner_next.count() > 0:
            expect(self.btn_partner_next).to_be_visible()

        if self.btn_partner_prev.count() > 0:
            expect(self.btn_partner_prev).to_be_visible()

    def click_partner_next(self):
        """Click Partner Next arrow."""
        if self.btn_partner_next.count() > 0:
            self.btn_partner_next.click(force=True)

    def click_partner_prev(self):
        """Click Partner Previous arrow."""
        if self.btn_partner_prev.count() > 0:
            self.btn_partner_prev.click(force=True)

    def verify_partner_pagination_visible(self):
        """Verify Partner pagination dots visible."""
        if self.partner_pagination.count() > 0:
            expect(
                self.partner_pagination.first
            ).to_be_visible()

    def verify_partner_next_button_working(self):
        """Verify clicking next changes active logo."""
        before = self.get_active_partner_index()

        self.click_partner_next()

        max_attempts = 10
        after = before

        for _ in range(max_attempts):
            self.page.wait_for_timeout(400)
            after = self.get_active_partner_index()

            if after != before:
                break

        assert before != after, (
            f"Expected next click to move slider. "
            f"Old: {before}, "
            f"New: {after}"
        )

    def verify_partner_slider_working(self):
        """Verify Partner slider auto moves."""
        before = self.get_active_partner_index()

        max_attempts = 10
        after = before

        for _ in range(max_attempts):
            self.page.wait_for_timeout(500)
            after = self.get_active_partner_index()

            if after != before:
                break

        assert after != before, (
            f"Expected partner slider to move. "
            f"Old: {before}, "
            f"New: {after}"
        )

    # ==================================================
    # Breadcrumb Methods
    # ==================================================

    def click_breadcrumb_home(self):
        """Click breadcrumb Home icon/link."""
        self.icon_breadcrumb_home.wait_for(
            state="visible"
        )
        self.icon_breadcrumb_home.click(force=True)