from playwright.sync_api import Page

from pages.base_page import BasePage


class HeaderComponent(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.search_box = page.get_by_placeholder("Search")
        self.search_button = page.locator("#search button")

    def get_search_box(self):
        return self.search_box

    def get_search_button(self):
        return self.search_button
