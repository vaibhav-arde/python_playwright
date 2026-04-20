# pages/home_page.py
# =====================

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
        self.dropdown_menu = page.locator("li.dropdown.open ul.dropdown-menu")
        self.lnk_register = self.dropdown_menu.get_by_role(
            "link", name="Register"
        )
        self.lnk_login = self.dropdown_menu.get_by_role(
            "link", name="Login"
        )
        self.txt_search_box = page.get_by_placeholder("Search")
        self.btn_search = page.locator("#search").get_by_role("button")
        self.main_menu = page.locator("#menu")
        self.footer = page.locator("footer")

        # ==================================================
        # Category Navigation
        # ==================================================
        self.lnk_desktops = page.locator(
            '#menu .nav > li > a:has-text("Desktops")'
        )
        self.lnk_pc = page.get_by_role(
            "link", name="PC (0)", exact=True
        )

        # ==================================================
        # Hero Slider
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
        self.list_slider_pagination = self.cnt_hero_slider.locator(
            ".swiper-pagination-bullet"
        )
        self.img_active_hero = self.cnt_hero_slider.locator(
            ".swiper-slide-active img, "
            ".swiper-slide-duplicate-active img"
        ).first

        # ==================================================
        # Featured Products
        # ==================================================
        self.txt_featured_heading = page.get_by_role(
            "heading", name="Featured"
        )
        self.list_featured_products = page.locator(
            "#content .product-layout"
        )

        # ==================================================
        # Partner Carousel
        # ==================================================
        self.partner_carousel = page.locator("#carousel0")
        self.partner_slides = self.partner_carousel.locator(
            ".swiper-slide"
        )
        self.active_partner = self.partner_carousel.locator(
            ".swiper-slide-active"
        ).first
        self.btn_partner_next = self.partner_carousel.locator(
            ".swiper-button-next"
        )
        self.btn_partner_prev = self.partner_carousel.locator(
            ".swiper-button-prev"
        )
        self.partner_pagination = self.partner_carousel.locator(
            ".swiper-pagination-bullet"
        )

        # ==================================================
        # Breadcrumb
        # ==================================================
        self.icon_breadcrumb_home = page.locator(
            "ul.breadcrumb li:first-child a"
        )

    # ==================================================
    # Header Actions
    # ==================================================

    def click_my_account(self):
        self.wait_visible(self.lnk_my_account)
        self.click(self.lnk_my_account)

    def click_register(self):
        self.wait_visible(self.dropdown_menu)
        self.click(self.lnk_register)

    def click_login(self):
        self.wait_visible(self.dropdown_menu)
        self.click(self.lnk_login)
        return LoginPage(self.page)

    # ==================================================
    # Visibility Methods
    # ==================================================

    def verify_logo_visible(self):
        self.verify_visible(self.img_logo)

    def verify_search_bar_visible(self):
        self.verify_visible(self.txt_search_box)

    def verify_main_menu_visible(self):
        self.verify_visible(self.main_menu)

    def verify_footer_visible(self):
        self.verify_visible(self.footer)

    def verify_slider_is_visible(self):
        self.verify_visible(self.cnt_hero_slider)

    def verify_featured_section_visible(self):
        self.verify_visible(self.txt_featured_heading)

    def verify_partner_carousel_visible(self):
        self.verify_visible(self.partner_carousel)

    def verify_partner_logos_visible(self):
        self.verify_visible(self.partner_slides.first)

    def verify_pagination_is_visible(self):
        if self.list_slider_pagination.count() > 0:
            self.verify_visible(
                self.list_slider_pagination.first
            )

    def verify_partner_pagination_visible(self):
        if self.partner_pagination.count() > 0:
            self.verify_visible(
                self.partner_pagination.first
            )

    # ==================================================
    # Grouped Methods
    # ==================================================

    def verify_home_page_ui(self):
        self.verify_logo_visible()
        self.verify_search_bar_visible()
        self.verify_main_menu_visible()
        self.verify_slider_is_visible()
        self.verify_featured_section_visible()
        self.verify_footer_visible()
        self.verify_partner_carousel_visible()
        self.verify_partner_logos_visible()

    def verify_partner_carousel_section(self):
        self.verify_partner_carousel_visible()
        self.verify_partner_logos_visible()
        self.verify_multiple_partner_logos()
        self.verify_partner_navigation_buttons_visible()
        self.verify_partner_pagination_visible()
        self.verify_partner_next_button_working()
        self.verify_partner_slider_working()

    # ==================================================
    # Search Methods
    # ==================================================

    def enter_product_name(self, product_name: str):
        self.fill(self.txt_search_box, product_name)

    def click_search(self):
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
        self.lnk_desktops.hover()
        self.lnk_pc.click()

    # ==================================================
    # Hero Slider Methods
    # ==================================================

    def get_slider_images_count(self) -> int:
        self.verify_visible(self.img_active_hero)
        return self.list_slider_images.count()

    def verify_slider_images_present(self):
        assert self.get_slider_images_count() > 0

    def verify_navigation_buttons_are_visible(self):
        if self.btn_slider_next.count() > 0:
            self.verify_visible(self.btn_slider_next)

        if self.btn_slider_prev.count() > 0:
            self.verify_visible(self.btn_slider_prev)

    def click_slider_next(self):
        if self.btn_slider_next.count() > 0:
            self.click(self.btn_slider_next)

    def click_slider_prev(self):
        if self.btn_slider_prev.count() > 0:
            self.click(self.btn_slider_prev)

    def get_active_image_src(self) -> str:
        return self.img_active_hero.get_attribute("src") or ""

    def verify_image_changed(self, previous_src: str):
        expect(self.img_active_hero).not_to_have_attribute(
            "src", previous_src
        )

    # ==================================================
    # Featured Products
    # ==================================================

    def get_featured_products_count(self) -> int:
        return self.list_featured_products.count()

    def verify_four_featured_products(self):
        assert self.get_featured_products_count() == 4

    # ==================================================
    # Partner Carousel
    # ==================================================

    def get_partner_logos_count(self) -> int:
        return self.partner_slides.count()

    def verify_multiple_partner_logos(self):
        assert self.get_partner_logos_count() >= 5

    def get_active_partner_index(self) -> str:
        return self.active_partner.get_attribute(
            "data-swiper-slide-index"
        ) or ""

    def verify_partner_navigation_buttons_visible(self):
        if self.btn_partner_next.count() > 0:
            self.verify_visible(self.btn_partner_next)

        if self.btn_partner_prev.count() > 0:
            self.verify_visible(self.btn_partner_prev)

    def click_partner_next(self):
        if self.btn_partner_next.count() > 0:
            self.btn_partner_next.click(force=True)

    def click_partner_prev(self):
        if self.btn_partner_prev.count() > 0:
            self.btn_partner_prev.click(force=True)

    def verify_partner_next_button_working(self):
        before = self.get_active_partner_index()
        self.click_partner_next()

        expect(self.active_partner).not_to_have_attribute(
            "data-swiper-slide-index",
            before,
        )

    def verify_partner_slider_working(self):
        before = self.get_active_partner_index()

        expect(self.active_partner).not_to_have_attribute(
            "data-swiper-slide-index",
            before,
        )

    # ==================================================
    # Breadcrumb
    # ==================================================

    def click_breadcrumb_home(self):
        self.wait_visible(self.icon_breadcrumb_home)
        self.icon_breadcrumb_home.click(force=True)