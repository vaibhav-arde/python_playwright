"""
TC_RF_020 - Verify 'Privacy Policy' checkbox is not selected by default.

Steps:
1. Click on 'My Account' Drop menu
2. Click on 'Register' option
3. Verify the 'Privacy Policy' checkbox is NOT checked by default (ER-1)
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.registration_page import RegistrationPage


@pytest.mark.sanity
def test_register_account_privacy_policy_checkbox_default_state(page):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    home_page.click_my_account()
    home_page.click_register()

    expect(registration_page.get_privacy_policy_checkbox()).not_to_be_checked()
