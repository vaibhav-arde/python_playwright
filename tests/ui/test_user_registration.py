# tests/ui/test_user_registration.py
# ==================================
# Validates the user registration UI flow.

from playwright.sync_api import expect
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from utils.helpers import RandomDataUtil


def test_user_registration_ui(page):
    """Verify that a new user can register successfully via the UI."""
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)
    random_data = RandomDataUtil()

    home_page.click_my_account()
    home_page.click_register()

    user_data = {
        "firstName": random_data.get_first_name(),
        "lastName": random_data.get_last_name(),
        "email": random_data.get_email(),
        "telephone": random_data.get_phone_number(),
        "password": random_data.get_password(),
    }

    registration_page.complete_registration(user_data)
    expect(registration_page.get_confirmation_msg()).to_have_text("Your Account Has Been Created!")
