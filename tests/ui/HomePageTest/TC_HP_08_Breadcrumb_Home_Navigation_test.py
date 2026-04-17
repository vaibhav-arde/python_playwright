"""
TC_HP_008 "(TS_011) Home Page"

Validate navigating to Home Page using 'Home' icon option
of the Breadcrumb in different pages of the Application

1. Open the Application URL and navigate to different pages
2. Click on 'Home' icon option in different pages
(Validate ER-1)
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage

@pytest.mark.ui
@pytest.mark.regression
def test_breadcrumb_home_navigation(page, base_url):
    page.goto(base_url)

    home_page = HomePage(page)

    # ===============================
    # Page 1: Register Page
    # ===============================
    home_page.click_my_account()
    home_page.click_register()

    home_page.click_breadcrumb_home()

    expect(home_page.img_logo).to_be_visible()

    # ===============================
    # Page 2: Login Page
    # ===============================
    home_page.click_my_account()
    home_page.click_login()

    home_page.click_breadcrumb_home()

    expect(home_page.img_logo).to_be_visible()