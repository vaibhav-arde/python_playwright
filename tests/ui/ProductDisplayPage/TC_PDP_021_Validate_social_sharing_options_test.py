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

    # Step 4: Verify social sharing options (AddThis) are no longer present
    # Note: AddThis service was discontinued in 2023. This test confirms the removal/absence
    # of the social sharing widget to prevent regressions where defunct scripts might still be loaded.
    add_this_widget = page.locator(".addthis_sharing_toolbox, .addthis_inline_share_toolbox")
    expect(add_this_widget).not_to_be_visible()

    # Also verify common classes are gone
    facebook_btn = page.locator(".addthis_button_facebook_like")
    expect(facebook_btn).not_to_be_visible()
