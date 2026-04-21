import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData
from utils import messages


@pytest.mark.ui
@pytest.mark.regression
def test_validate_average_review_display(page: Page):
    """
    Test Case ID: TC_PDP_014
    Validate average of the user reviews should be dispalyed under the 'Add to Cart' button of the Product Display page

    Steps:
        1. Open the Application URL (handled by navigate_to_base_url fixture)
        2. Enter any existing Product name into the Search text box field
        3. Click on the button having search icon
        4. Click on the Product displayed in the Search results
        5. Check the average and number of reviews on the Product Display page

    Expected Result:
        Correct average review and the number of reviews count should be displayed
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

    # Step 5: Check the average and number of reviews
    # Validate ER-1: Correct average review (stars block) is displayed
    expect(product_page.pnl_rating_summary).to_be_visible(), messages.PDP_RATING_SUMMARY_NOT_VISIBLE

    # Validate ER-1: The number of reviews count ("X reviews") should be displayed
    expect(product_page.lbl_review_count).to_be_visible(), messages.PDP_REVIEW_COUNT_NOT_VISIBLE

    # Advanced assertion: grab the text to verify it contains the word "review"
    review_count_text = product_page.lbl_review_count.text_content().strip()
    assert (
        "review" in review_count_text.lower()
    ), f"Expected 'reviews' count in text but got '{review_count_text}'"
