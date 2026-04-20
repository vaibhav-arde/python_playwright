import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData
from utils import messages

@pytest.mark.ui
@pytest.mark.regression
def test_validate_review_text_character_range(page: Page):
    
    """
    Test Case ID: TC_PDP_018
    Validate the review text given while writing is accepted according to the specified number of characters (25 to 1000)

    Steps:
        1. Open the Application URL
        2. Search for a product (iMac)
        3. Select the product from search results
        4. Select the Reviews tab of the Product
        5. Provide Name and Ratings
        6. Provide review text outside the 25-1000 range and click 'Continue'

    Expected Result:
        Warning message 'Warning: Review Text must be between 25 and 1000 characters!' should be displayed.
    """
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)

    product_name = TestData.PRODUCT_NAME_IMAC

    home_page.enter_product_name(product_name)
    home_page.click_search()

    product_in_results = search_results_page.is_product_exist(product_name)
    assert product_in_results is not None, messages.SEARCH_RESULT_PRODUCT_NOT_FOUND.format(keyword=product_name)

    expected_product_name = search_results_page.get_text(product_in_results).strip()
    search_results_page.select_product(expected_product_name)

    product_page.click_review_tab()

    # Test Case: Review text too short
    product_page.enter_review_name(TestData.REVIEW_AUTHOR_NAME)
    product_page.select_review_rating(TestData.REVIEW_RATING_VALUE)
    product_page.enter_review_text(TestData.REVIEW_TEXT_TOO_SHORT)
    product_page.submit_review()

    actual_warning_text = product_page.get_review_warning_text()
    assert actual_warning_text == messages.WARN_REVIEW_RANGE, \
        f"Expected '{messages.WARN_REVIEW_RANGE}', but got '{actual_warning_text}'"

    # Test Case: Review text too long
    product_page.enter_review_text(TestData.REVIEW_TEXT_TOO_LONG)
    product_page.submit_review()

    actual_warning_text = product_page.get_review_warning_text()
    assert actual_warning_text == messages.WARN_REVIEW_RANGE, \
        f"Expected '{messages.WARN_REVIEW_RANGE}', but got '{actual_warning_text}'"
