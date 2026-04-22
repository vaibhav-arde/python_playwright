import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData


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

    home_page.open_home_page()
    home_page.enter_product_name(TestData.PRODUCT_NAME_IMAC)
    home_page.click_search()

    search_results_page.select_product(TestData.PRODUCT_NAME_IMAC)

    # Step 4: Verify social sharing options (AddThis) are no longer present
    # Note: AddThis service was discontinued in 2023. This test confirms the removal/absence
    # of the social sharing widget to prevent regressions where defunct scripts might still be loaded.

    # Use POM methods instead of direct locator objects or CSS strings in test case
    expect(product_page.get_social_sharing_widget()).not_to_be_visible()

    # Also verify common classes are gone
    expect(product_page.get_facebook_like_button()).not_to_be_visible()
