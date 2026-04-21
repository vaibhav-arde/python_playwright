import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData, UIAvailability
from utils import messages


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.sanity
def test_validate_the_availability_status(page: Page):
    """
    Test Case ID: TC_PDP_003
    Validate the availability status of the Product in the Product Display Page.
    """
    # Initialize Page Objects
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)

    # Note: conftest.py's navigate_to_base_url fixture automatically navigates to the base URL

    # Step 1: Enter any existing Product name into the Search text box field
    home_page.enter_product_name(TestData.PRODUCT_NAME_IMAC)

    # Step 2: Click on the button having search icon
    home_page.click_search()

    # Step 3: Click on the Product displayed in the Search results
    search_results_page.select_product(TestData.PRODUCT_NAME_IMAC)

    # Step 4: Check the different availability status of the Products in the displayed Product Display Page

    # Validate ER-1: Proper availability statuses like In Stock, Out of Stock and Limited Stock
    # should be displayed in the Availability section

    expect(product_page.lbl_product_availability).to_be_visible()
    actual_availability = product_page.get_product_availability()

    # Check that availability is populated and follows supported status values.
    assert actual_availability != "", messages.AVAILABILITY_STATUS_EMPTY
    assert (
        actual_availability in UIAvailability.VALID_PRODUCT_STATUSES
    ), messages.AVAILABILITY_STATUS_UNEXPECTED.format(status=actual_availability)
