"""
Test Case: End-to-End Flow

===========================================
Test Steps
===========================================
1. Register a new user.
2. Logout.
3. Login with the registered credentials.
4. Search and add a product to cart.
5. Verify cart contents.
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.logout_page import LogoutPage
from pages.my_account_page import MyAccountPage
from pages.product_page import ProductPage
from pages.registration_page import RegistrationPage
from pages.search_results_page import SearchResultsPage
from utils.config import Config
from utils.helpers import RandomDataUtil


@pytest.mark.end_to_end
def test_end_to_end_flow(page):
    """
    End-to-End Test Flow:
    1. Register a new user.
    2. Logout.
    3. Login with the registered credentials.
    4. Search and add a product to cart.
    5. Verify cart contents.
    """

    # Step 1: Register a new account
    registered_email, registered_password = perform_registration(page)

    # Step 2: Logout after registration
    perform_logout(page)

    # Step 3: Login with registered email
    perform_login(page, registered_email, registered_password)

    # Step 4: Search product and add to cart
    add_product_to_cart(page)

    # Step 5: Verify cart details
    verify_shopping_cart(page)


# ---- Helper Functions ----


def perform_registration(page):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    home_page.click_my_account()
    home_page.click_register()

    random_data = RandomDataUtil()

    first_name = random_data.get_first_name()
    last_name = random_data.get_last_name()
    email = random_data.get_email()
    phone = random_data.get_phone_number()
    password = random_data.get_password()

    registration_page.set_first_name(first_name)
    registration_page.set_last_name(last_name)
    registration_page.set_email(email)
    registration_page.set_telephone(phone)
    registration_page.set_password(password)
    registration_page.set_confirm_password(password)
    registration_page.set_privacy_policy()
    registration_page.click_continue()

    confirmation_msg = registration_page.get_confirmation_msg()
    expect(confirmation_msg).to_have_text("Your Account Has Been Created!")

    return email, password


def perform_logout(page):
    my_account = MyAccountPage(page)
    logout_page = LogoutPage(page)

    my_account.click_logout()
    expect(logout_page.get_continue_button()).to_be_visible(timeout=5000)

    logout_page.click_continue()
    expect(page).to_have_title("Your Store")


def perform_login(page, email, password):
    home = HomePage(page)
    home.click_my_account()
    home.click_login()

    login = LoginPage(page)
    login.login(email, password)

    my_account_page = MyAccountPage(page)
    expect(my_account_page.get_my_account_page_heading()).to_be_visible(timeout=5000)


def add_product_to_cart(page):
    product_name = Config.product_name
    quantity = Config.product_quantity

    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    home_page.enter_product_name(product_name)
    home_page.click_search()

    expect(search_results_page.get_search_results_page_header()).to_be_visible(timeout=5000)
    expect(search_results_page.is_product_exist(product_name)).to_be_visible(timeout=5000)

    product_page = search_results_page.select_product(product_name)
    product_page.set_quantity(quantity)
    product_page.add_to_cart()

    expect(product_page.get_confirmation_message()).to_be_visible(timeout=10000)


def verify_shopping_cart(page):
    product_page = ProductPage(page)
    product_page.click_items_to_navigate_to_cart()

    shopping_cart = product_page.click_view_cart()

    expect(shopping_cart.get_total_price()).to_have_text(Config.total_price)
