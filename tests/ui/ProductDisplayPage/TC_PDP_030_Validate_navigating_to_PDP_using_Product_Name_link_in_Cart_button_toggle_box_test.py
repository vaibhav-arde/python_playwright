import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData
from utils.config import Config
from utils import messages


@pytest.mark.ui
@pytest.mark.regression
def test_validate_navigating_to_pdp_using_product_name_link_in_cart_button_toggle_box(page: Page):
    """
    Test Case ID: TC_PDP_030
    Validate navigating to the Product Display page by using the Product Name link in the 'Cart' button toggle box.
    """
    home_page = HomePage(page)
    login_page = LoginPage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)

    product_name = TestData.PRODUCT_NAME_IMAC

    # Step 1: Open the Application URL and Login
    home_page.click_my_account()
    home_page.click_login()
    login_page.login(Config.email, Config.password)

    # Step 2-3: Enter Product Name and Click Search icon
    home_page.enter_product_name(product_name)
    home_page.click_search()

    # Step 4: Click on 'Add to Cart' option on the product that is displayed in the Search Results
    search_results_page.select_product(product_name)
    product_page.add_to_cart()
    expect(product_page.get_confirmation_message()).to_be_visible()

    # Step 5: Click on 'Cart' button which is in black color beside the search icon button on the top of the page
    home_page.click_cart_button()

    # Step 6 (ER-1): Click on the Product Name link in the displayed toggle box
    new_product_page = home_page.click_cart_name_link()

    # Validation: User should be taken to the Product Display page of the Product
    expect(new_product_page.lbl_product_name).to_be_visible()
    actual_product_name = new_product_page.get_product_name()
    assert actual_product_name == product_name, messages.PDP_PRODUCT_NAME_MISMATCH.format(
        expected=product_name, actual=actual_product_name
    )
