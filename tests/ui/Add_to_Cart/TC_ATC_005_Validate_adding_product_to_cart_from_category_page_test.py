import pytest
from playwright.sync_api import Page, expect

from pages.home_page import HomePage
from pages.category_page import CategoryPage
from pages.shopping_cart_page import ShoppingCartPage
from utils import messages
from utils.constants import TestData, UILabels

@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.add_to_cart
def test_atc_005_validate_adding_product_to_cart_from_category_page(page: Page):
    """
    TC_ATC_005: Validate adding the product to Cart from Products displayed in category or sub-category page
    
    Steps:
    1. Open the Application URL (Handled by navigate_to_base_url fixture)
    2. Hover the mouse on 'Desktops'
    3. Click on 'Show All Desktops' option
    4. Select 'Mac' subcategory option from the left side options
    5. Click on 'Add to Cart' button for 'iMac' (Validate ER-1)
    6. Click on the 'shopping cart!' link in the success message (Validate ER-2)
    """
    
    home_page = HomePage(page)
    category_page = CategoryPage(page)
    
    # Step 1: Open the Application URL is handled by autouse fixture.
    # We can explicitly ensure we are on the home page if needed.
    home_page.open_home_page()
    
    # Step 2 & 3: Hover 'Desktops' and click 'Show All Desktops'
    home_page.hover_menu(TestData.MENU_DESKTOPS)
    home_page.click_sub_menu(TestData.SUB_MENU_SHOW_ALL_DESKTOPS)
    
    # Step 4: Select 'Mac' subcategory from the left side
    category_page.select_subcategory(TestData.SUB_MENU_MAC)
    
    # Step 5: Click on 'Add to Cart' button for 'iMac'
    product_name = TestData.PRODUCT_NAME_IMAC
    category_page.click_add_to_cart(product_name)
    
    # ER-1: Success message should be displayed
    # OpenCart success message often contains extra whitespace/newlines, so we check for containment or use a flexible regex
    expect(category_page.get_confirmation_message()).to_contain_text(product_name)
    expect(category_page.get_confirmation_message()).to_contain_text(messages.PDP_ADD_TO_CART_SUCCESS_PREFIX)
    expect(category_page.get_confirmation_message()).to_contain_text(messages.PDP_ADD_TO_CART_SUCCESS_SUFFIX)

    # Step 6: Click on the 'shopping cart!' link in the displayed success message
    shopping_cart_page = category_page.click_shopping_cart_link()
    
    # ER-2: Product should be successfully displayed in the 'Shopping Cart' page
    expect(shopping_cart_page.lbl_cart_page_header).to_contain_text(UILabels.CART_PAGE_HEADING)
    
    # Verify the product is in the cart table
    is_present = shopping_cart_page.is_product_in_cart(product_name)
    assert is_present, f"Product '{product_name}' should be present in the shopping cart"
