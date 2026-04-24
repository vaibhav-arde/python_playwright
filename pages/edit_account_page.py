# pages/edit_account_page.py
# =====================
# Page Object for the Edit Account Information Page.
# Used to verify persisted user details after registration.

from playwright.sync_api import Page
from pages.base_page import BasePage


class EditAccountPage(BasePage):
    """Page Object Model for the Edit Account Information page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.txt_firstname = page.locator("#input-firstname")
        self.txt_lastname = page.locator("#input-lastname")
        self.txt_email = page.locator("#input-email")
        self.txt_telephone = page.locator("#input-telephone")
        self.msg_heading = page.get_by_role("heading", name="My Account Information")
        self.btn_continue = page.get_by_role("button", name="Continue")
        self.msg_success = page.locator("div.alert-success")
        self.err_firstname = self.get_warning("input-firstname")
        self.err_lastname = self.get_warning("input-lastname")
        self.err_email = self.get_warning("input-email")
        self.err_telephone = self.get_warning("input-telephone")
        self.btn_back = page.get_by_role("link", name="Back", exact=True)
        # Breadcrumb container
        self.breadcrumb = page.locator(".breadcrumb")

        # Home (icon link → no name, so use CSS)
        self.lnk_home = self.breadcrumb.locator("li:first-child a")

        # Account (role-based)
        self.lnk_account = self.breadcrumb.get_by_role("link", name="Account", exact=True)

        # Edit Information (role-based)
        self.lnk_edit_info = self.breadcrumb.get_by_role("link", name="Edit Information")

    def get_page_heading(self):
        """Returns the page heading locator."""
        return self.msg_heading

    def get_page_title(self) -> str:
        """Returns the page title."""
        return self.get_title()

    # ===== Accessor Methods =====

    def get_first_name(self) -> str:
        """Returns the value in the First Name field."""
        return self.txt_firstname.input_value()

    def get_last_name(self) -> str:
        """Returns the value in the Last Name field."""
        return self.txt_lastname.input_value()

    def get_email(self) -> str:
        """Returns the value in the E-Mail field."""
        return self.txt_email.input_value()

    def get_telephone(self) -> str:
        return self.txt_telephone.input_value()

    # ===== Actions =====

    def update_account_information(self, user):
        self.txt_firstname.fill(user["firstName"])
        self.txt_lastname.fill(user["lastName"])
        self.txt_email.fill(user["email"])
        self.txt_telephone.fill(user["telephone"])

    def update_email(self, email: str):
        self.txt_email.fill(email)
        self.click(self.btn_continue)

    def click_continue(self):
        """Click on the Continue button."""
        self.click(self.btn_continue)

    def get_success_message(self):
        """Returns the success message locator."""
        return self.msg_success

    def clear_account_info_fields(self):
        self.txt_firstname.clear()
        self.txt_lastname.clear()
        self.txt_email.clear()
        self.txt_telephone.clear()

    def clear_email_field(self):
        self.txt_email.clear()

    def get_placeholder(self, field_id: str) -> str:
        return self.page.locator(f"#{field_id}").get_attribute("placeholder")

    def is_field_mandatory(self, field_id: str) -> bool:
        field = self.page.locator(f"#{field_id}")
        parent = field.locator("xpath=ancestor::div[contains(@class,'form-group')]")
        classes = parent.get_attribute("class")
        return "required" in classes

    def verify_mandatory_fields(self, account_fields: dict):
        for field_id, data in account_fields.items():
            if data.get("mandatory"):
                assert self.is_field_mandatory(
                    field_id
                ), f"{data['label']} is not marked as mandatory"

    def get_email_validation_message(self) -> str:
        return self.txt_email.evaluate("el => el.validationMessage")

    def click_back(self):
        """Click on the Back button."""
        self.click(self.btn_back)

    def get_account_information(self) -> dict:
        """Return current values of account fields."""
        return {
            "firstName": self.txt_firstname.input_value(),
            "lastName": self.txt_lastname.input_value(),
            "email": self.txt_email.input_value(),
            "telephone": self.txt_telephone.input_value(),
        }

    def validate_breadcrumb(self):
        """Validate breadcrumb links on My Account Information page."""
        from playwright.sync_api import expect

        expect(self.breadcrumb).to_be_visible()
        expect(self.lnk_home).to_be_visible()
        expect(self.lnk_account).to_be_visible()
        expect(self.lnk_edit_info).to_be_visible()
