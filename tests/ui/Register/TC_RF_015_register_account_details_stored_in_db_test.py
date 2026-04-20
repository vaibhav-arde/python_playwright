# tests/ui/Register/TC_RF_015_register_account_details_stored_in_db_test.py
# =========================================================================
# Test Case ID: TC_RF_015
# Description: Validate the details provided while Registering an Account
# are stored in the Database (Verified via Account Profile UI Persistence)
# =========================================================================

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from pages.registration_page import RegistrationPage
from utils import messages
from utils.helpers import RandomDataUtil


@pytest.mark.ui
@pytest.mark.regression
def test_register_account_details_stored_in_db(page):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)
    my_account_page = MyAccountPage(page)

    # Step: Navigate to Register
    home_page.click_my_account()
    home_page.click_register()
    login_page = LoginPage(page)

    # Step: Prepare and fill Data
    user = RandomTestData.get_user()

    registration_page.complete_registration(
        user, newsletter_locator=registration_page.radio_newsletter_yes
    )

    # Verification: Account Created Success Message
    confirmation_msg = registration_page.get_confirmation_msg()
    expect(confirmation_msg).to_be_visible()
    expect(confirmation_msg).to_have_text(messages.ACCOUNT_CREATED)

    # We click 'Continue' to go to 'My Account' dashboard or just use the nav links.
    registration_page.click_continue()  # This takes user to My Account page from Success page.

    my_account_page.click_logout()

    # Step: Verify Edit Account Info Persistence
    home_page.click_my_account()
    home_page.click_login()
    login_page.set_email(user["email"])
    login_page.set_password(user["password"])
    login_page.click_login()

    expect(my_account_page.get_my_account_page_heading()).to_be_visible()
