import re
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from utils.constants import TestData
from utils.messages import SUCCESS_WISH_LIST
from utils.random_test_data import RandomTestData


@pytest.mark.sanity
@pytest.mark.ui
def test_add_featured_product_to_wishlist(page):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    # Pre-requisite: Register new user (ensures dynamic login and clean state)
    home_page.click_my_account()
    home_page.click_register()

    user_data = RandomTestData.get_user()
    registration_page.complete_registration(user_data)

    # Step 1: Click on the 'Store logo'
    home_page.click_logo()

    # Validate ER-1: User should be taken to Home page
    # Best Practice: Use regex to match both the base URL and the 'common/home' route
    expect(page).to_have_url(re.compile(r".*(/|common/home)$"))

    # Step 2: Scroll down to the 'Featured' section
    home_page.scroll_to_featured_section()

    # Step 3: Click on 'Add to Wish List' on a product in the 'Featured' section
    product_name = TestData.PRODUCT_MACBOOK
    home_page.add_featured_product_to_wishlist(product_name)

    # Validate ER-2: Success message
    success_msg_locator = home_page.get_success_message()
    expected_msg = SUCCESS_WISH_LIST.format(product_name=product_name)
    expect(success_msg_locator).to_contain_text(expected_msg)

    # Step 4: Click on the 'wish list!' link in the displayed success message
    wishlist_page = home_page.click_wishlist_link_in_success_message()

    # Validate ER-3: Product should be successfully displayed in the 'My Wish List' page
    expect(wishlist_page.is_product_in_wishlist(product_name)).to_be_visible()
