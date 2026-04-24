from playwright.sync_api import Page
from pages.base_page import BasePage
from utils import messages


class ChangePasswordPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.txt_password = page.locator("#input-password")
        self.txt_confirm_password = page.locator("#input-confirm")
        self.btn_continue = page.locator("input[value='Continue']")
        self.err_pass_required = page.get_by_text(messages.WARN_PASSWORD_REQUIRED)
        self.err_pass_mismatch = page.get_by_text(messages.WARN_PASSWORD_MISMATCH)
        self.lbl_password = page.locator('label[for="input-password"]')
        self.lbl_confirm_password = page.locator('label[for="input-confirm"]')
        self.msg_success = page.locator(".alert-success")

    def fill_new_password_details(self, new_password: str):
        """Fill new password details and click continue."""
        self.fill(self.txt_password, new_password)
        self.fill(self.txt_confirm_password, new_password)
        self.click(self.btn_continue)

    def fill_new_password(self, new_password: str):
        """Fill new password details and click continue."""
        self.fill(self.txt_password, new_password)
        self.fill(self.txt_confirm_password, new_password)

    def get_password_field(self):
        """Return the label for the Password field."""
        return self.txt_password

    def get_confirm_password_field(self):
        """Return the label for the Confirm Password field."""
        return self.txt_confirm_password

    def fill_different_password_details(self, new_password: str, confirm_new_password: str):
        """Fill new password details and click continue."""
        self.fill(self.txt_password, new_password)
        self.fill(self.txt_confirm_password, confirm_new_password)
        self.click(self.btn_continue)

    def get_success_message(self):
        """Return the success message locator."""
        return self.msg_success

    def click_continue(self):
        """Click the Continue button."""
        self.click(self.btn_continue)

    def get_pass_required_error(self):
        """Return the password required error message locator."""
        return self.err_pass_required

    def get_pass_mismatch_error(self):
        """Return the password mismatch error message locator."""
        return self.err_pass_mismatch

    def is_field_mandatory(self, field_name: str) -> bool:
        """
        Check if a field is marked as mandatory by verifying the ::before pseudo-element.
        field_name can be 'password' or 'confirm'.
        """
        locator = self.lbl_password if field_name == "password" else self.lbl_confirm_password

        # Check if parent has 'required' class and ::before has '*' and is red
        return locator.evaluate("""(element) => {
            const style = window.getComputedStyle(element, '::before');
            const content = style.getPropertyValue('content');
            const color = style.getPropertyValue('color');
            const isRequired = element.parentElement.classList.contains('required');

            // content usually comes with quotes from getComputedStyle, e.g., '"* "' or 'none'
            return isRequired && content.includes('*') && (color === 'rgb(255, 0, 0)' || color === 'red');
        }""")
