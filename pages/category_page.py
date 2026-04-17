# pages/category_page.py

from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class CategoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.no_products_msg = page.locator("text=There are no products")
        self.continue_btn = page.get_by_role("link", name="Continue")

    def verify_empty_category(self):
        expect(self.no_products_msg).to_be_visible()

    def click_continue(self):
        expect(self.continue_btn).to_be_visible()
        self.continue_btn.click()