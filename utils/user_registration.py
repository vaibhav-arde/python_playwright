# # utils/user_registration.py
# # =====================
# # Faker-based user registration module.
# # Generates random user data and performs UI registration
# # so the same credentials can be reused for login/session storage.

import logging

from utils.helpers import RandomDataUtil
from playwright.sync_api import Page, expect

from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from utils import messages

logger = logging.getLogger(__name__)


def generate_user_data() -> dict:
    """
    Generate random user data using Faker.
    Returns a dict with keys: firstName, lastName, email, telephone, password.
    """
    random_data = RandomDataUtil()

    user_data = {
        "firstName": random_data.get_first_name(),
        "lastName": random_data.get_last_name(),
        "email": random_data.get_email(),
        "telephone": random_data.get_phone_number(),
        "password": random_data.get_password(length=10),
    }

    logger.info(f"Generated user data — email: {user_data['email']}")
    return user_data


def register_user(page: Page, user_data: dict) -> None:
    """
    Perform user registration via UI using the provided user data.

    Steps:
        1. Navigate to Home → My Account → Register.
        2. Fill all mandatory fields from user_data.
        3. Accept privacy policy and submit.
        4. Assert the success confirmation message.
    """
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    logger.info("Starting user registration flow")

    home_page.click_my_account()
    home_page.click_register()

    registration_page.set_first_name(user_data["firstName"])
    registration_page.set_last_name(user_data["lastName"])
    registration_page.set_email(user_data["email"])
    registration_page.set_telephone(user_data["telephone"])
    registration_page.set_password(user_data["password"])
    registration_page.set_confirm_password(user_data["password"])
    registration_page.set_privacy_policy()
    registration_page.click_continue()

    # Verify registration succeeded
    confirmation_msg = registration_page.get_confirmation_msg()
    expect(confirmation_msg).to_have_text(messages.ACCOUNT_CREATED, timeout=10000)

    logger.info(f"User registered successfully — email: {user_data['email']}")
