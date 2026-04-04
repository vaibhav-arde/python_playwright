from playwright.sync_api import Page
from pages.base_page import BasePage


class NewsletterPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.msg_newsletter_heading = page.get_by_role("heading", name="Newsletter Subscription")
        self.radio_newsletter_yes = page.locator("input[name='newsletter'][value='1']")
        self.radio_newsletter_no = page.locator("input[name='newsletter'][value='0']")
        self.btn_continue = page.get_by_role("button", name="Continue")

    # ===== Actions =====
    def set_newsletter(self, value: str):
        """Select newsletter option."""
        self.select_radio(self.radio_newsletter_yes, self.radio_newsletter_no, value)

    def click_continue(self):
        """Click the Continue button."""
        self.click(self.btn_continue)

    # ===== Validations =====
    def get_newsletter_yes_radio(self):
        return self.radio_newsletter_yes

    def get_newsletter_no_radio(self):
        return self.radio_newsletter_no

    def get_newsletter_heading(self):
        return self.msg_newsletter_heading