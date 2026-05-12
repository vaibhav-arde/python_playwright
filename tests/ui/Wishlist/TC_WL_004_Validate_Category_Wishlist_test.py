import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from utils.constants import TestData, CategoryNames
from utils.messages import SUCCESS_WISH_LIST


@pytest.mark.sanity
@pytest.mark.ui
def test_add_category_product_to_wishlist(authenticated_page):
    home_page = HomePage(authenticated_page)

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
    success_msg_locator = home_page.get_success_message()
    expected_msg = SUCCESS_WISH_LIST.format(product_name=product_name)
    expect(success_msg_locator).to_contain_text(expected_msg)

    # Step 5: Click on the 'wish list!' link in the success message
    wishlist_page = home_page.click_wishlist_link_in_success_message()

    # Validate ER-2: Product successfully displayed in My Wish List
    expect(wishlist_page.is_product_in_wishlist(product_name)).to_be_visible()
