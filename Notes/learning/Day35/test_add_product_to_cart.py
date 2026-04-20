import pytest
from cartpage import CartPage
from homepage import HomePage
from loginpage import LoginPage
from playwright.sync_api import Page, expect


@pytest.mark.parametrize(
    "username, password, product_name", [("pavanol", "test@123", "Samsung galaxy s6")]
)
def test_user_can_login_and_add_product_to_cart(page: Page, username, password, product_name):
    # Navigate to site
    page.goto("https://www.demoblaze.com/index.html")

    # --- Login Page ---
    login_page = LoginPage(page)
    login_page.click_login_link()
    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_login_button()

    # --- Home Page ---
    home_page = HomePage(page)
    home_page.add_product_to_cart(product_name)
    page.wait_for_timeout(3000)
    home_page.goto_cart()
    page.wait_for_timeout(3000)

    # --- Cart Page ---
    cart_page = CartPage(page)
    product_in_cart = cart_page.check_product_in_cart(product_name)

    # expect()
    expect(product_in_cart).to_be_visible()
