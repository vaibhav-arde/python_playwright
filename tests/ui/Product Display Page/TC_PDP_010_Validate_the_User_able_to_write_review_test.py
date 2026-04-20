import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData
from utils import messages


@pytest.mark.ui
@pytest.mark.regression
def test_validate_user_able_to_write_review(page: Page):
    """
    Test Case ID: TC_PDP_010
    Validate that the User is able to write a review for the Product
    from the 'Reviews' tab of the Product Display Page.

    Steps:
        1. Navigate to the base URL (handled by navigate_to_base_url fixture)
        2. Search for an existing product by name
        3. Click the product in Search results to open the Product Display Page
        4. Click on the 'Reviews' tab
        5. Enter reviewer name in the 'Your Name' field
        6. Enter review text in the 'Your Review' textarea
        7. Select a star rating
        8. Click the 'Continue' button to submit the review

    Expected Result:
        Success message 'Thank you for your review. It has been submitted to
        the webmaster for approval.' should be displayed.
    """
    # Initialize Page Objects
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)

    product_name = TestData.PRODUCT_NAME_APPLE_CINEMA_30

    # Step 2: Enter a product name into the Search text box field
    home_page.enter_product_name(product_name)

    # Step 3: Click Search button
    home_page.click_search()

    # Validate product appears in search results and capture exact name
    product_in_results = search_results_page.is_product_exist(product_name)
    assert product_in_results is not None, messages.SEARCH_RESULT_PRODUCT_NOT_FOUND.format(
        keyword=product_name
    )
    expected_product_name = search_results_page.get_text(product_in_results).strip()
    assert expected_product_name != "", messages.SEARCH_RESULT_PRODUCT_NAME_EMPTY

    # Step 4: Click on the product in search results to open the Product Display Page
    search_results_page.select_product(expected_product_name)

    # Step 5: Click the 'Reviews' tab on the Product Display Page
    expect(product_page.lnk_review_tab).to_be_visible(), messages.PDP_REVIEW_TAB_NOT_VISIBLE
    product_page.click_review_tab()

    # Step 6: Enter reviewer name into 'Your Name' field
    product_page.enter_review_name(TestData.REVIEW_AUTHOR_NAME)

    # Step 7: Enter review text into 'Your Review' textarea
    product_page.enter_review_text(TestData.REVIEW_TEXT_VALID)

    # Step 8: Select a star rating
    product_page.select_review_rating(TestData.REVIEW_RATING_VALUE)

    # Step 9: Click 'Continue' to submit the review
    product_page.submit_review()

    # Validate ER-1: Review success alert should be displayed
    review_alert = product_page.get_review_success_alert()
    expect(review_alert).to_be_visible(), messages.PDP_REVIEW_ALERT_NOT_VISIBLE

    # Validate ER-1: Success alert text should match the expected confirmation message
    actual_success_text = product_page.get_review_success_text()
    assert actual_success_text == messages.PDP_REVIEW_SUCCESS_TEXT, (
        messages.PDP_REVIEW_SUCCESS_TEXT_MISMATCH.format(
            expected=messages.PDP_REVIEW_SUCCESS_TEXT,
            actual=actual_success_text,
        )
    )
