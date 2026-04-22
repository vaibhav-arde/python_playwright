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
@pytest.mark.smoke
def test_register_account_details_stored_in_db(page):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)
    my_account_page = MyAccountPage(page)
    login_page = LoginPage(page)

    home_page.click_my_account()
    home_page.click_register()

    user = RandomDataUtil().get_user()

    registration_page.complete_registration(
        user,
        newsletter_locator=registration_page.radio_newsletter_yes,
    )

    confirmation_msg = registration_page.get_confirmation_msg()
    expect(confirmation_msg).to_be_visible()
    expect(confirmation_msg).to_have_text(messages.ACCOUNT_CREATED)

    registration_page.click_continue()

    my_account_page.click_logout()

    home_page.click_my_account()
    home_page.click_login()

    login_page.set_email(user["email"])
    login_page.set_password(user["password"])
    login_page.click_login()

    expect(my_account_page.get_my_account_page_heading()).to_be_visible()
