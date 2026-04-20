import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData
from utils import messages

@pytest.mark.ui
@pytest.mark.regression
def test_validate_social_sharing_options(page: Page):
    """
    Test Case ID: TC_PDP_021
    Validate proper options for liking, tweeting, sharing the Product Display page on social platforms
    """
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)

    product_name = TestData.PRODUCT_NAME_IMAC

    home_page.open_home_page()
    home_page.enter_product_name(product_name)
    home_page.click_search()

    search_results_page.select_product(product_name)

    # Step 4: Check social options presence
    # Since AddThis service is discontinued, icons are not visible/rendered.
    # We verify the placeholder elements are attached to the DOM.
    expect(product_page.sns_facebook).to_be_attached(timeout=10000)
    expect(product_page.sns_twitter).to_be_attached(timeout=10000)
    expect(product_page.sns_pinterest).to_be_attached(timeout=10000)
