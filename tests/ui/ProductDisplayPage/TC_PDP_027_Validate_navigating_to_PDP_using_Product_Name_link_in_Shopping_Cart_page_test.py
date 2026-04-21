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
def test_validate_navigating_to_pdp_using_product_name_link_in_shopping_cart_page(page: Page):
    """
    Test Case ID: TC_PDP_027
    Validate navigating to the Product Display page by using the Product Name link in the 'Shopping Cart' page.
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

    # Step 4: Click on the Product displayed in the Search results
    search_results_page.select_product(product_name)

    # Step 5: Click on 'Add to Cart' button
    product_page.add_to_cart()

    # Step 6: Click on 'shopping cart!' link from the displayed success page
    expect(product_page.get_confirmation_message()).to_be_visible()
    shopping_cart_page = product_page.click_shopping_cart_link()

    # Step 7 (ER-1): Click on the Product Name link from the displayed Shopping Cart page
    new_product_page = shopping_cart_page.click_product_name()

    # Validation: User should be taken to the Product Display page of the Product
    expect(new_product_page.lbl_product_name).to_be_visible()
    actual_product_name = new_product_page.get_product_name()
    assert actual_product_name == product_name, messages.PDP_PRODUCT_NAME_MISMATCH.format(
        expected=product_name, actual=actual_product_name
    )
