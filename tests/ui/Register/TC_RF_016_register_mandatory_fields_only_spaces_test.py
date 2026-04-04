"""
TC_RF_016: Mandatory fields should NOT accept only spaces.
After submitting the form with spaces-only input, validation
warnings must appear for each mandatory field.
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from utils import messages
from utils.constants import UIRoutes

# Single space — ensures even non-trimmed fields fail their minimum-length validation
SPACES_ONLY = "   "


@pytest.mark.regression
def test_register_mandatory_fields_only_spaces(page, base_url):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    # Step 1-3: Navigate to Register page
    home_page.click_my_account()
    home_page.click_register()

    # Step 4: Fill all mandatory fields with SPACES
    registration_page.set_first_name(SPACES_ONLY)
    registration_page.set_last_name(SPACES_ONLY)
    registration_page.set_email(SPACES_ONLY)
    registration_page.set_telephone(SPACES_ONLY)
    registration_page.set_password(SPACES_ONLY)
    registration_page.set_confirm_password(SPACES_ONLY)

    # Step 5: Accept Privacy Policy
    registration_page.set_privacy_policy()

    # Step 6: Click Continue
    registration_page.click_continue()

    # ER-1: Validate that warning messages are displayed

    # First Name
    expect(registration_page.get_warning("input-firstname")).to_have_text(messages.WARN_FIRST_NAME)

    # Last Name
    expect(registration_page.get_warning("input-lastname")).to_have_text(messages.WARN_LAST_NAME)

    # E-Mail
    expect(registration_page.get_warning("input-email")).to_have_text(messages.WARN_EMAIL)

    # Telephone
    expect(registration_page.get_warning("input-telephone")).to_have_text(messages.WARN_TELEPHONE)

    # Password
    expect(registration_page.get_warning("input-password")).to_have_text(messages.WARN_PASSWORD)

    # Validate that the URL remains on the registration page
    expected_url = f"{base_url}{UIRoutes.REGISTER}"
    expect(page).to_have_url(expected_url)
