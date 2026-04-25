from playwright.sync_api import Page

from pages.base_page import BasePage


class ContactUsPage(BasePage):
    """Page Object Model for Contact Us page."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ===== Locators =====
        self.heading_contact_us = page.locator("#content h1")
        self.input_name = page.locator("#input-name")
        self.input_email = page.locator("#input-email")
        self.input_enquiry = page.locator("#input-enquiry")
        self.btn_submit = page.locator('input[type="submit"]')

        # Success Page
        self.success_heading = page.locator("#content h1")
        self.btn_continue = page.get_by_role("link", name="Continue")

    # ===== Verification Methods =====

    def verify_contact_page_opened(self):
        """Verify Contact Us page is opened."""
        assert self.is_visible(self.heading_contact_us)

    def verify_contact_details_and_fields_displayed(self):
        """Verify required details and fields are displayed."""
        assert self.is_visible(self.heading_contact_us)
        assert self.is_visible(self.input_name)
        assert self.is_visible(self.input_email)
        assert self.is_visible(self.input_enquiry)
        assert self.is_visible(self.btn_submit)

    def verify_all_mandatory_fields_validation(self):
        """Verify all mandatory field warnings are displayed."""
        assert self.is_visible(self.page.locator("#input-name + .text-danger"))
        assert self.is_visible(self.page.locator("#input-email + .text-danger"))
        assert self.page.locator(".text-danger").count() >= 1

    def verify_success_message_visible(self):
        """Verify Contact Us success page is displayed."""
        assert self.is_visible(self.success_heading)
        assert self.is_visible(self.btn_continue)

    # ===== Action Methods =====

    def enter_name(self, name: str):
        """Enter customer name."""
        self.fill(self.input_name, name)

    def enter_email(self, email: str):
        """Enter customer email."""
        self.fill(self.input_email, email)

    def enter_enquiry(self, enquiry: str):
        """Enter enquiry message."""
        self.fill(self.input_enquiry, enquiry)

    def click_submit(self):
        """Click Submit button."""
        self.click(self.btn_submit)

    def submit_contact_form(self, name: str, email: str, enquiry: str):
        """Fill and submit Contact Us form."""
        self.enter_name(name)
        self.enter_email(email)
        self.enter_enquiry(enquiry)
        self.click_submit()

    def submit_empty_contact_form(self):
        """Submit form without entering values."""
        self.click_submit()

    def click_continue(self):
        """Click Continue button."""
        self.click(self.btn_continue)
