import pytest
from playwright.sync_api import expect, Page
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData
from utils import messages

@pytest.mark.ui
@pytest.mark.regression
def test_validate_review_text_length_validation(page: Page):
    """
    Test Case ID: TC_PDP_018
    Validate the review text given while writing is accepted according to the specified number of characters.

    Steps:
        1. Open the Application URL.
        2. Enter any existing Product name into the Search text box field.
        3. Click on the button having search icon.
        4. Click on the Product displayed in the Search results.
        5. Select the Reviews tab of the Product in the displayed 'Product Display' page.
        6. Provide Name and Ratings.
        7. Provide review text which is not according to the specified range (25 to 1000 characters) and click 'Continue'.

    Expected Result:
        Proper warning message with the text - 'Warning: Review Text must be between 25 and 1000 characters!' should be displayed.
    """
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)

    # Step 2: Enter product name into the Search text box field
    home_page.enter_product_name(TestData.PRODUCT_NAME_IMAC)

    # Step 3: Click on the button having search icon
    home_page.click_search()

    # Step 4: Click on the Product displayed in the Search results
    product_in_results = search_results_page.is_product_exist(TestData.PRODUCT_NAME_IMAC)
    assert product_in_results is not None, messages.SEARCH_RESULT_PRODUCT_NOT_FOUND.format(
        keyword=TestData.PRODUCT_NAME_IMAC
    )
    expected_product_name = search_results_page.get_text(product_in_results).strip()
    search_results_page.select_product(expected_product_name)

    # Step 5: Select the Reviews tab of the Product
    expect(product_page.lnk_review_tab).to_be_visible(), messages.PDP_REVIEW_TAB_NOT_VISIBLE
    product_page.click_review_tab()

    # Step 6: Provide Name and Ratings
    product_page.enter_review_name(TestData.REVIEW_AUTHOR_NAME)
    product_page.select_review_rating(TestData.REVIEW_RATING_VALUE)

    # Step 7: Provide review text that is too short (less than 25 characters)
    # Using TestData.REVIEW_TEXT_TOO_SHORT from constants (e.g., "Short review")
    product_page.enter_review_text(TestData.REVIEW_TEXT_TOO_SHORT)
    product_page.submit_review()

    # Validate ER-1: Proper warning message should be displayed
    warning_alert = product_page.get_review_warning_alert()
    expect(warning_alert).to_be_visible(), messages.PDP_REVIEW_WARNING_ALERT_NOT_VISIBLE

    actual_warning_text = product_page.get_review_warning_text()
    expected_warning = "Warning: Review Text must be between 25 and 1000 characters!"

    assert expected_warning in actual_warning_text, \
        f"Expected warning message '{expected_warning}' not found. Actual: '{actual_warning_text}'"
