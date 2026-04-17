import re
import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData
from utils import messages


@pytest.mark.ui
@pytest.mark.regression
def test_validate_review_link_under_add_to_cart(page: Page):
    """
    Test Case ID: TC_PDP_013
    Validate 'Write a review' link under 'Add to Cart' button on the 'Product Display' page

    Steps:
        1. Open the Application URL (handled by navigate_to_base_url fixture)
        2. Enter any existing Product name into the Search text box field
        3. Click on the button having search icon
        4. Click on the Product displayed in the Search results
        5. Click on 'Write a review' link under 'Add to Cart' button of the 'Product Display' page

    Expected Result:
        'Reviews' tab in the Product Display page should come to the focus.
    """
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)

    product_name = TestData.PRODUCT_NAME_IMAC

    # Step 2: Enter Product name into the Search text box field
    home_page.enter_product_name(product_name)

    # Step 3: Click Search button
    home_page.click_search()

    # Verify product in search results and capture its name
    product_in_results = search_results_page.is_product_exist(product_name)
    assert product_in_results is not None, messages.SEARCH_RESULT_PRODUCT_NOT_FOUND.format(
        keyword=product_name
    )
    expected_product_name = product_in_results.text_content().strip()
    assert expected_product_name != "", messages.SEARCH_RESULT_PRODUCT_NAME_EMPTY

    # Step 4: Click on the Product displayed in the Search results
    search_results_page.select_product(expected_product_name)

    # Validate PDP opened by waiting for heading and checking product name
    expect(product_page.lbl_product_name).to_be_visible()
    actual_product_name = product_page.get_product_name()
    assert actual_product_name == expected_product_name, messages.PDP_PRODUCT_NAME_MISMATCH.format(
        expected=expected_product_name, actual=actual_product_name
    )

    # Step 5: Click on 'Write a review' link under 'Add to Cart' button
    expect(product_page.lnk_write_review).to_be_visible()
    product_page.click_write_review_link()

    # Validate ER-1: 'Reviews' tab in the Product Display page should come to the focus
    # (The review panel should visually switch to visible)
    try:
        expect(product_page.pnl_review).to_be_visible(timeout=5000)
    except AssertionError:
        pytest.fail(messages.PDP_REVIEW_PANEL_NOT_VISIBLE)
    
    # Advanced assertion: Assert that the parent <li> of the review tab carries the 'active' class
    # The xpath=.. robustly fetches the immediate parent element
    parent_li = product_page.lnk_review_tab.locator("xpath=..")
    expect(parent_li).to_have_class(re.compile(r"active"))
