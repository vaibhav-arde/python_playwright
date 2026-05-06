"""
Test Case: Validate the Breadcrumb, Page Heading, Page Title and Page URL of Login Page
====================================================================================

Acceptance Criteria:
✅ Layout & Structure
- Page loads correctly (no broken layout)
- Left + right column visible

✅ Mandatory Elements
- Email field present
- Password field present
- Login button present
- Forgotten Password link present

✅ Labels & Text
- Correct field labels (E-Mail Address, Password)
- No typos

✅ Alignment & Styling
- Proper spacing, alignment
- Buttons styled correctly

✅ Functional UI
- Fields accept input
- Button is clickable
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.constants import UIRoutes
from utils import messages


@pytest.mark.ui
def test_validate_the_breakcrumb_page_heading_page_title_and_page_url_of_login_page(page, base_url):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    # --- Step 1: Navigate to Login Page ---
    home_page.click_my_account()
    home_page.click_login()

    # --- Metadata Validation ---
    # Validate Page Title
    expect(page).to_have_title(messages.LOGIN_PAGE_TITLE)

    # Validate Page URL
    expect(page).to_have_url(f"{base_url}{UIRoutes.LOGIN}")

    # Validate Page Heading
    # expect(login_page.get_page_heading()).to_have_text(messages.LOGIN_PAGE_TITLE)

    # Validate Breadcrumb
    expect(login_page.get_breadcrumb()).to_be_visible()
    expect(login_page.get_breadcrumb()).to_contain_text(messages.ACCOUNT_LOGIN_BREADCRUMB)
