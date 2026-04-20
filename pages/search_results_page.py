# pages/search_results_page.py
# =====================
# Page Object for the Search Results Page.
# Inherits from BasePage for reusable UI interaction methods.

from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.product_page import ProductPage
from utils.config import SORT_CONFIG
from utils.assertions import extract_price


class SearchResultsPage(BasePage):
    """Page Object Model class for the Search Results Page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.search_page_header = page.locator("#content").get_by_role("heading", level=1)
        self.search_products = page.get_by_role("heading", level=4).get_by_role("link")
        self.msg_empty_search = page.get_by_text(
            "There is no product that matches the search criteria."
        )
        self.txt_search_criteria = page.get_by_role("textbox", name="Search Criteria")
        self.drp_category = page.get_by_role("combobox").filter(
            has=page.get_by_role("option", name="All Categories")
        )
        self.btn_search_criteria = page.get_by_role("button", name="Search")
        self.chk_search_in_descriptions = page.get_by_label("Search in product descriptions")
        self.chk_search_in_subcategories = page.get_by_role(
            "checkbox", name="Search in subcategories"
        )
        self.btn_list_view = page.get_by_role("button").filter(has=page.locator("i.fa-th-list"))
        self.btn_grid_view = page.get_by_role("button").filter(has=page.locator("i.fa-th"))
        self.product_thumb = page.locator(".product-thumb")
        self.btn_add_to_cart = page.get_by_role("button", name="Add to Cart")
        self.btn_wish_list = page.get_by_role("button", name="Add to Wish List")
        self.btn_compare = page.get_by_role("button", name="Compare this Product")
        self.msg_success = page.locator(".alert-success")
        self.link_product_compare = page.get_by_role("link", name="Product Compare")
        self.drp_sort = page.get_by_label("Sort By:")
        self.product_prices = page.locator(".price")
        self.drp_limit = page.get_by_role("combobox", name="Show")
        self.breadcrumb = page.locator("ul.breadcrumb")
        self.home_link = page.locator("ul.breadcrumb a[href*='route=common/home']")
        self.search_link = page.get_by_role("link", name="Search")

    # ===== Page Header =====

    def get_search_results_page_header(self):
        """Returns the header element of the search results page."""
        return self.search_page_header

    def get_search_criteria_textbox(self):
        """Returns the search criteria text box locator on the search results page."""
        return self.txt_search_criteria

    def get_empty_search_message(self):
        """Returns the locator for the empty search results message."""
        return self.msg_empty_search

    def get_category_dropdown(self):
        """Returns the locator for the category dropdown."""
        return self.drp_category

    def get_search_button(self):
        """Returns the locator for the search button in criteria section."""
        return self.btn_search_criteria

    def get_search_in_descriptions_checkbox(self):
        """Returns the locator for the 'Search in product descriptions' checkbox."""
        return self.chk_search_in_descriptions

    def get_search_in_subcategories_checkbox(self):
        """Returns the locator for the 'Search in subcategories' checkbox."""
        return self.chk_search_in_subcategories

    def get_list_view_button(self):
        """Returns the locator for the list view toggle button."""
        return self.btn_list_view

    def get_grid_view_button(self):
        """Returns the locator for the grid view toggle button."""
        return self.btn_grid_view

    def get_sort_dropdown(self):
        """Returns the locator for the sort by dropdown."""
        return self.drp_sort

    def get_limit_dropdown(self):
        """Returns the locator for the limit (show) dropdown."""
        return self.drp_limit

    # ===== Actions =====

    def enter_search_criteria(self, criteria: str):
        """Enter text into the Search Criteria text box."""
        self.fill(self.txt_search_criteria, criteria)

    def select_category(self, category_name: str):
        """Select a category from the Category dropdown using role-based locator."""
        # Find the option by name with exact match to handle "Mac" vs "Macs" and whitespace
        option = self.drp_category.get_by_role("option", name=category_name, exact=True)
        value = option.get_attribute("value")
        self.select_option(self.drp_category, value=value)

    def select_search_in_product_descriptions(self):
        """Select the 'Search in product descriptions' checkbox."""
        self.check(self.chk_search_in_descriptions)

    def select_search_in_subcategories(self):
        """Select the 'Search in subcategories' checkbox."""
        self.check(self.chk_search_in_subcategories)

    def click_search_criteria_button(self):
        """Click the Search button next to the Search Criteria text box."""
        self.click(self.btn_search_criteria)

    def click_list_view(self):
        """Click the List view button."""
        self.click(self.btn_list_view)

    def click_grid_view(self):
        """Click the Grid view button."""
        self.click(self.btn_grid_view)

    def get_product_image(self, product_name: str):
        """Returns the locator for a product image by name."""
        return self.page.get_by_role("img", name=product_name)

    def click_product_image(self, product_name: str):
        """Click on the product image."""
        self.click(self.get_product_image(product_name).first)

    def click_product_link(self, product_name: str):
        """Click on the product name link."""
        self.click(self.page.get_by_role("link", name=product_name, exact=True).first)

    def get_product_container(self, product_name: str):
        """Returns the locator for a product container by its name."""
        return self.product_thumb.filter(
            has=self.page.get_by_role("link", name=product_name, exact=True)
        )

    def click_add_to_cart(self, product_name: str):
        """Click 'Add to Cart' for a specific product."""
        self.click(
            self.get_product_container(product_name).get_by_role("button", name="Add to Cart")
        )

    def click_wishlist(self, product_name: str):
        """Click 'Add to Wish List' for a specific product."""
        # Note: Tooltip plugin removes 'title' attribute, so we filter by icon class
        self.click(
            self.get_product_container(product_name)
            .get_by_role("button")
            .filter(has=self.page.locator("i.fa-heart"))
        )

    def click_compare(self, product_name: str):
        """Click 'Compare this Product' for a specific product."""
        # Note: Tooltip plugin removes 'title' attribute, so we filter by icon class
        self.click(
            self.get_product_container(product_name)
            .get_by_role("button")
            .filter(has=self.page.locator("i.fa-exchange"))
        )

    # ===== Product Verification =====

    def is_product_exist(self, product_name: str) -> bool:
        return self.search_products.filter(has_text=product_name).count() > 0

    # ===== Product Selection =====

    def select_product(self, product_name: str) -> ProductPage | None:
        """Select a product from search results by name."""
        count = self.search_products.count()
        for i in range(count):
            product = self.search_products.nth(i)
            title = product.text_content()
            if title and title.strip() == product_name:
                self.click(product)
                return ProductPage(self.page)
        return None

    # ===== Product Count =====

    def get_product_count(self):
        """Returns all product locators found in search results."""
        return self.search_products

    def get_products_by_search_term(self, search_term: str):
        """Returns a locator of products filtered by the given search term text."""
        return self.search_products.filter(has_text=search_term)

    def get_success_message(self, product_name: str):
        return self.msg_success.filter(has=self.page.get_by_role("link", name=product_name))

    def click_product_compare_link(self):
        self.click(self.link_product_compare)

    # ===== Sorting Methods =====

    def select_sort_choice(self, sort_choice: str):
        """Select a sorting option from the 'Sort By' dropdown."""
        self.select_option(self.drp_sort, label=sort_choice)
        self.page.wait_for_load_state("networkidle")

    def get_product_names(self):
        """Returns a list of product names in lowercase."""
        return [v.strip().lower() for v in self.search_products.all_text_contents()]

    def get_product_prices(self):
        """Returns a list of numerical product prices."""
        return [extract_price(t) for t in self.product_prices.all_text_contents()]

    def get_product_ratings(self):
        """Returns a list of product ratings based on star count."""
        return [product.locator(".fa-star").count() for product in self.product_thumb.all()]

    def verify_products_sorted(self, sort_option: str):
        """Verify that products are sorted correctly based on the selected option."""
        if sort_option not in SORT_CONFIG:
            raise ValueError(f"Unsupported sort option: {sort_option}")

        config = SORT_CONFIG[sort_option]

        # Use refined waiting strategy: wait for product thumb visibility
        self.product_thumb.first.wait_for(state="visible")

        actual = config["getter"](self)

        # Robustness check: Ensure result list is not empty
        assert actual, f"Product list is empty, cannot verify sorting for '{sort_option}'"

        expected = sorted(actual, reverse=config["reverse"])

        assert actual == expected, (
            f"Sorting failed for '{sort_option}'\n" f"Actual: {actual}\nExpected: {expected}"
        )

    def select_limit(self, value: str):
        """Select number of products to display from 'Show' dropdown."""
        self.select_option(self.drp_limit, label=value)
        self.page.wait_for_load_state("networkidle")

    def validate_breadcrumb(self):
        """Validate breadcrumb options"""
        assert self.home_link.is_visible()
        assert self.search_link.is_visible()
