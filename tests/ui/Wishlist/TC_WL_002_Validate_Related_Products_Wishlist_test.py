import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.constants import TestData
from utils.messages import (
    ERR_PRODUCT_NOT_FOUND,
    ERR_RELATED_PRODUCT_NAME_NOT_FOUND,
    SUCCESS_WISH_LIST,
)


@pytest.mark.sanity
@pytest.mark.ui
def test_add_related_product_to_wishlist(authenticated_page):
    home_page = HomePage(authenticated_page)
    search_results_page = SearchResultsPage(authenticated_page)

    # Step 1 & 2: Search for product
    home_page.enter_product_name(TestData.PRODUCT_IMAC)
    home_page.click_search()

    # Step 3: Click on the Product in Search Results
    product_page = search_results_page.select_product(TestData.PRODUCT_IMAC)
    assert product_page is not None, ERR_PRODUCT_NOT_FOUND.format(
        product_name=TestData.PRODUCT_IMAC
    )

    # Step 4: Click Add to Wishlist on a Related Product
    added_product_name = product_page.add_related_product_to_wishlist(index=0)
    assert added_product_name, ERR_RELATED_PRODUCT_NAME_NOT_FOUND

    # Validate ER-1: Success message
    success_msg_locator = product_page.get_confirmation_message()
    expected_msg = SUCCESS_WISH_LIST.format(product_name=added_product_name)
    expect(success_msg_locator).to_contain_text(expected_msg)

    # Step 5: Click 'wish list!' link in message
    wishlist_page = product_page.click_wishlist_link_in_message()

    # Validate ER-2: Product successfully displayed in My Wish List
    expect(wishlist_page.is_product_in_wishlist(added_product_name)).to_be_visible()
