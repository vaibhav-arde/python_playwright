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
def test_validate_review_count_in_tab(page: Page):
    """
    Test Case ID: TC_PDP_015
    Validate the count of reviews should be displayed in the 'Reviews' tab label of the Product Display page

    Steps:
        1. Open the Application URL (handled by navigate_to_base_url fixture)
        2. Enter any existing Product name into the Search text box field
        3. Click on the button having search icon
        4. Click on the Product displayed in the Search results
        5. Check the count of reviews in the 'Reviews' tab label in the Product Display page

    Expected Result:
        Correct count of reviews should be displayed in the 'Reviews' tab label of the Product Display Page.
    """
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)

    # Step 2: Enter Product name into the Search text box field
    home_page.enter_product_name(TestData.PRODUCT_NAME_IMAC)

    # Step 3: Click Search button
    home_page.click_search()

    # Verify product in search results and capture its name
    product_in_results = search_results_page.is_product_exist(TestData.PRODUCT_NAME_IMAC)
    assert product_in_results is not None, messages.SEARCH_RESULT_PRODUCT_NOT_FOUND.format(
        keyword=TestData.PRODUCT_NAME_IMAC
    )
    expected_product_name = search_results_page.get_text(product_in_results).strip()
    assert expected_product_name != TestData.EMPTY_VALUE, messages.SEARCH_RESULT_PRODUCT_NAME_EMPTY

    # Step 4: Click on the Product displayed in the Search results
    search_results_page.select_product(expected_product_name)

    # Validate PDP opened by waiting for heading and checking product name
    expect(product_page.lbl_product_name).to_be_visible()
    actual_product_name = product_page.get_product_name()
    assert actual_product_name == expected_product_name, messages.PDP_PRODUCT_NAME_MISMATCH.format(
        expected=expected_product_name, actual=actual_product_name
    )

    # Step 5: Check the count of reviews in the 'Reviews' tab label
    expect(product_page.lnk_review_tab).to_be_visible(), messages.PDP_REVIEW_TAB_NOT_VISIBLE

    tab_text = product_page.get_text(product_page.lnk_review_tab).strip()

    # Validate ER-1: Reviews tab contains the count, e.g. "Reviews (0)"
    assert re.search(
        r"Reviews \(\d+\)", tab_text, re.IGNORECASE
    ), f"{messages.PDP_REVIEW_TAB_COUNT_MISSING}. Actual text: '{tab_text}'"
