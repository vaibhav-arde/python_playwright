import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage
from pages.registration_page import RegistrationPage
from utils import messages
from utils.helpers import RandomDataUtil


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.smoke
def test_user_registration_no_newsletter(page):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)
    my_account_page = MyAccountPage(page)

    home_page.click_my_account()
    home_page.click_register()

    user = RandomDataUtil().get_user()

    registration_page.complete_registration(
        user,
        newsletter_locator=registration_page.radio_newsletter_no,
    )

    confirmation_msg = registration_page.get_confirmation_msg()
    expect(confirmation_msg).to_have_text(messages.ACCOUNT_CREATED)

    registration_page.click_continue()

    expect(my_account_page.get_my_account_page_heading()).to_have_text(messages.MY_ACCOUNT_HEADING)

    my_account_page.click_newsletter_subscription()

    expect(my_account_page.radio_newsletter_no).to_be_checked()
