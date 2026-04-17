"""TC_HP_002 "(TS_011) Home Page"
Validate navigating to Home Page from 'Order Success'
page 1. Open the Application URL and place an order 
1. Click on 'Continue' button in the 'Success' page (Validate ER-1)
Product Name: iMac"""

import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from utils.config import Config
from utils.constants import expected_title


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.xfail()
def test_navigate_home_from_cart(page):
    """Verify that clicking 'Continue Shopping' on the Shopping Cart page
    navigates the user back to the Home Page."""

    product_name = Config.product_name

    # Step 1: Application URL is opened via navigate_to_base_url fixture

    # Step 2 & 3: Search for a product
    home_page = HomePage(page)
    home_page.enter_product_name(product_name)
    search_results_page = home_page.click_search()

    # Step 4: Select the product and add to cart
    product_page = search_results_page.select_product(product_name)
    product_page.add_to_cart()

    # Step 5: Click on 'shopping cart' link in the success message
    shopping_cart_page = product_page.click_shopping_cart_in_success_message()