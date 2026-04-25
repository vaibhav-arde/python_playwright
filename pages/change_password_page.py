from playwright.sync_api import Page
from pages.base_page import BasePage
from utils import change_password_constants


class ChangePasswordPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.txt_password = page.locator("#input-password")
        self.txt_confirm_password = page.locator("#input-confirm")
        self.btn_continue = page.locator("input[value='Continue']")
        self.err_pass_required = page.get_by_text(change_password_constants.WARN_PASSWORD_REQUIRED)
        self.err_pass_mismatch = page.get_by_text(change_password_constants.WARN_PASSWORD_MISMATCH)
        self.lbl_password = page.locator('label[for="input-password"]')
        self.lbl_confirm_password = page.locator('label[for="input-confirm"]')
        self.msg_success = page.locator(".alert-success")
        self.btn_back = page.get_by_role("link", name="Back")
        self.breadcrumb_wrapper = page.locator("ul.breadcrumb")
        self.page_heading = page.locator("div#content h1")
        self.Accoutn_breadcrumb = self.breadcrumb_wrapper.get_by_role("link", name="Account")
        self.change_password_breadcrumb = self.breadcrumb_wrapper.get_by_role(
            "link", name="Change Password"
        )
        self.legend_your_password = page.locator("fieldset legend")

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

    def get_page_heading(self):
        """Return the page heading."""
        return self.page_heading

    def get_password_field_value(self):
        """Return the value of the Password field."""
        return self.txt_password.input_value()

    def get_confirm_password_field(self):
        """Return the label for the Confirm Password field."""
        return self.txt_confirm_password

    def get_confirm_password_field_value(self):
        """Return the value of the Confirm Password field."""
        return self.txt_confirm_password.input_value()

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

    def get_breadcrumb_items(self):
        """Return list of breadcrumb items."""
        return self.breadcrumb_wrapper

    def get_account_breadcrumb(self):
        """Return the Account breadcrumb locator."""
        self.click(self.Accoutn_breadcrumb)

    def get_change_password_breadcrumb(self):
        """Return the Change Password breadcrumb locator."""
        self.click(self.change_password_breadcrumb)

    def get_pass_required_error(self):
        """Return the password required error message locator."""
        return self.err_pass_required

    def get_pass_mismatch_error(self):
        """Return the password mismatch error message locator."""
        return self.err_pass_mismatch

    def click_back(self):
        """Click the Back button."""
        self.click(self.btn_back)

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
