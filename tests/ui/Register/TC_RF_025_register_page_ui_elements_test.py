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
import re

from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage


@pytest.mark.sanity
def test_register_page_ui_elements(page):

    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    # Step 1 & 2
    home_page.click_my_account()
    home_page.click_register()

    # ✅ Page Heading
    expect(registration_page.get_page_heading()).to_have_text("Register Account")

    # ✅ URL Validation
    expect(page).to_have_url(re.compile(".*route=account/register.*"))
    
    # ✅ Page Title
    expect(page).to_have_title("Register Account")

    # ✅ Breadcrumb Validation
    breadcrumb = registration_page.get_breadcrumb()
    expect(breadcrumb).to_contain_text("Register")