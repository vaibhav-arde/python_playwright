import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData
from utils import messages

@pytest.mark.ui
@pytest.mark.regression
def test_validate_submit_review_without_mandatory_fields(page: Page):
    """
    Test Case ID: TC_PDP_017
    Validate submitting a review without filling the mandatory fields

    Steps:
        1. Open the Application URL
        2. Search for a product (iMac)
        3. Select the product from search results
        4. Select the Reviews tab of the Product
        5. Click 'Continue' without providing Name, Review, and Ratings

    Expected Result:
        Proper warning messages informing the User to fill the mandatory fields should be displayed.
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

    expect(product_page.lbl_product_name).to_be_visible()

    product_page.click_review_tab()
    product_page.submit_review()

    warning_alert = product_page.get_review_warning_alert()
    expect(warning_alert).to_be_visible(), messages.PDP_REVIEW_WARNING_ALERT_NOT_VISIBLE

    actual_warning_text = product_page.get_review_warning_text()
    assert "Warning" in actual_warning_text, messages.PDP_REVIEW_WARNING_MISSING_KEYWORD.format(
        keyword="Warning", actual=actual_warning_text
    )
