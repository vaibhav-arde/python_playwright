from playwright.sync_api import Page
from pages.base_page import BasePage

class ChangePasswordPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.txt_password = page.locator("#input-password")
        self.txt_confirm_password = page.locator("#input-confirm")
        self.btn_continue = page.locator("input[value='Continue']")

    def fill_new_password_details(self, new_password: str):
        """Fill new password details and click continue."""
        self.fill(self.txt_password, new_password)
        self.fill(self.txt_confirm_password, new_password)
        self.click(self.btn_continue)

    def get_success_message(self):
        """Return the success message locator."""
        return self.msg_success
    
    def click_continue(self):
        """Click the Continue button."""
        self.click(self.btn_continue)