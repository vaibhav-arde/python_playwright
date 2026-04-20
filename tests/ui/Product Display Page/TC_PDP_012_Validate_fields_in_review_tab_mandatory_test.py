import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData
from utils import messages


@pytest.mark.ui
@pytest.mark.regression
def test_validate_fields_in_review_tab_mandatory(page: Page):
    """
    Test Case ID: TC_PDP_012
    Validate all the fields in the 'Review' tab are mandatory fields

    Steps:
        1. Open the Application URL (handled by navigate_to_base_url fixture)
        2. Enter any existing Product name into the Search text box field
        3. Click on the button having search icon
        4. Click on the Product displayed in the Search results
        5. Click on the Reviews tab of the Product
        6. Click the 'Continue' button without entering any details

    Expected Result:
        All the fields in the Reviews tab should be mandatory fields (warning alert displayed)
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
    expected_product_name = search_results_page.get_text(product_in_results).strip()
    assert expected_product_name != "", messages.SEARCH_RESULT_PRODUCT_NAME_EMPTY

    # Step 4: Click on the Product displayed in the Search results
    search_results_page.select_product(expected_product_name)

    # Validate PDP opened by waiting for heading and checking product name
    expect(product_page.lbl_product_name).to_be_visible()
    actual_product_name = product_page.get_product_name()
    assert actual_product_name == expected_product_name, messages.PDP_PRODUCT_NAME_MISMATCH.format(
        expected=expected_product_name, actual=actual_product_name
    )

    # Step 5: Click on the Reviews tab
    expect(product_page.lnk_review_tab).to_be_visible(), messages.PDP_REVIEW_TAB_NOT_VISIBLE
    product_page.click_review_tab()

    # Step 6: Click Continue WITHOUT entering any information
    product_page.submit_review()

    # Validate ER-1: Warning message displayed indicating fields are mandatory
    warning_alert = product_page.get_review_warning_alert()
    expect(warning_alert).to_be_visible(), messages.PDP_REVIEW_WARNING_ALERT_NOT_VISIBLE
    
    actual_warning_text = product_page.get_review_warning_text()
    assert "Warning" in actual_warning_text, messages.PDP_REVIEW_WARNING_MISSING_KEYWORD.format(
        keyword="Warning", actual=actual_warning_text
    )
