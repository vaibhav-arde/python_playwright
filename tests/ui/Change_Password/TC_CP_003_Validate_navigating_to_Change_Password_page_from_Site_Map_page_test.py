import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.sitemap_page import SitemapPage
from pages.registration_page import RegistrationPage
from utils.messages import CHANGE_PASSWORD_PAGE_TITLE
from utils.user_registration import generate_user_data, register_user


@pytest.mark.ui
def test_change_password_from_my_account_using_sitemap_option(page):
    """
    Test Case: TC_CP_003 - Validate navigating to Change Password page using sitemap option
    """
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)
    sitemap_page = SitemapPage(page)

    # Step 1: Generate random user data and register
    user_data = generate_user_data()
    register_user(page, user_data)
    
    # After registration, click continue to go to My Account

    registration_page.click_continue()
    
    # 1. Click on 'Site Map' footer option
    home_page.click_site_map()
    
    # 2. Click on 'Password' link in the displayed 'Site Map' page
    sitemap_page.click_password()

    # Acceptance Criteria - User should be navigated to 'Change Password' page
    expect(page).to_have_title(CHANGE_PASSWORD_PAGE_TITLE)
