"""
1. Click on 'My Account' Drop menu
2. Click on 'Register' option

Expected:
- Breadcrumb is correct
- Page heading is "Register Account"
- URL contains 'route=account/register'
- Page title is correct
"""

import pytest

from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from utils.constants import UILabels, UITitles, UIRoutes


@pytest.mark.sanity
def test_register_page_ui_elements(page):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    # Step 1 & 2
    home_page.click_my_account()
    home_page.click_register()

    # ✅ Page Heading
    expect(registration_page.lbl_page_heading).to_have_text(UILabels.REGISTER_PAGE_HEADING)

    # ✅ URL Validation
    assert page.url.endswith(UIRoutes.REGISTER)

    # Page Title
    expect(page).to_have_title(UITitles.REGISTER_PAGE_TITLE)

    # Breadcrumb
    expect(registration_page.lnk_breadcrumb).to_contain_text(UILabels.REGISTER_BREADCRUMB)
