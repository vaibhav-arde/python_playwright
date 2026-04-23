"""
TC_WL_004_Validate adding the product to Wish List from the Products displayed in the category or sub-category page

Pre-requisites :
Open the Application URL and login

Test Steps :
1. Hover the mouse on any of the menu option say 'Desktops'
2. Click on 'Show All Desktops' option
3. Select 'Mac' subcategory option from the left side options
4. Click on 'Add to Wish List' option that is available on any of the Products of the displayed Category or Sub-category pages (Validate ER-1)
5. Click on the 'wish list!' link in the displayed success message (Validate ER-2)

Acceptance Criteria :
1. Success message with text - 'Success: You have added Product Name to your wish list!' should be displayed
2. Product should be successfully displayed in the 'My Wish List' page
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from utils.constants import TestData, CategoryNames
from utils.messages import SUCCESS_WISH_LIST
from utils.random_test_data import RandomTestData


@pytest.mark.sanity
@pytest.mark.ui
def test_add_category_product_to_wishlist(page):
    home_page = HomePage(page)
    registration_page = RegistrationPage(page)

    # Pre-requisite: Register new user (ensures dynamic login and clean state)
    home_page.click_my_account()
    home_page.click_register()

    user_data = RandomTestData.get_user()
    registration_page.complete_registration(user_data)

    # Step 1 & 2: Open category menu and Click 'Show All'
    home_page.open_category_menu(CategoryNames.DESKTOPS)
    category_page = home_page.click_show_all_in_category(CategoryNames.DESKTOPS)

    # Step 3: Select subcategory from the left side options
    category_page.select_subcategory_from_sidebar(CategoryNames.MAC)

    # Step 4: Click 'Add to Wish List' on a product
    # Using iMac which is standard in the Mac subcategory
    product_name = TestData.PRODUCT_IMAC
    category_page.add_product_to_wishlist(product_name)

    # Validate ER-1: Success message
    # Success message locator is shared in the header/base layout
    success_msg_locator = home_page.get_success_message()
    expected_msg = SUCCESS_WISH_LIST.format(product_name=product_name)
    expect(success_msg_locator).to_contain_text(expected_msg)

    # Step 5: Click on the 'wish list!' link in the success message
    wishlist_page = home_page.click_wishlist_link_in_success_message()

    # Validate ER-2: Product successfully displayed in My Wish List
    expect(wishlist_page.is_product_in_wishlist(product_name)).to_be_visible()
