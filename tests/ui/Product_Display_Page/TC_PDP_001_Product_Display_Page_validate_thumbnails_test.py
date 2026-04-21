import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.constants import TestData, UIIndexes, UIAttributes
from utils import messages


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.sanity
def test_product_display_page_validate_thumbnails(page: Page):
    """
    Test Case ID: TC_PDP_001
    Validate the Thumbnails of the Product displayed in the Product Display Page
    """
    # Initialize Page Objects
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)

    # Step 1 cont'd: Enter any existing Product name into the Search text box field
    home_page.enter_product_name(TestData.PRODUCT_NAME_IMAC)

    # Step 2: Click on the button having search icon
    home_page.click_search()

    # Step 3: Click on the Product displayed in the Search results
    search_results_page.select_product(TestData.PRODUCT_NAME_IMAC)

    # Step 4: Click on the main bigger sized Thumbnail image displayed on the 'Product Display Page'
    product_page.click_main_thumbnail()
    
    # Validate ER-1: Light box view of the main Thumbnail image should be displayed
    lightbox = product_page.get_lightbox()
    expect(lightbox).to_be_visible()
    
    # Store initial image src to assert navigation works
    initial_image_src = product_page.get_element_attribute(product_page.get_lightbox_image(), UIAttributes.IMAGE_SOURCE)

    # Step 5: Click on '<' and '>' options
    product_page.click_lightbox_next()
    
    # Validate ER-2: User should be able to navigate to other thumbnail images
    next_image_src = product_page.get_element_attribute(product_page.get_lightbox_image(), UIAttributes.IMAGE_SOURCE)
    assert next_image_src != (initial_image_src or ""), messages.THUMBNAIL_SRC_SHOULD_CHANGE_ON_NEXT

    # Click prev to ensure dual navigation works
    product_page.click_lightbox_prev()

    # Step 6: Click on 'x' option
    product_page.click_lightbox_close()
    
    # Validate ER-3: Light box view should close and focus goes to Product Display Page
    expect(lightbox).to_be_hidden()

    # Step 7: Click on the normal sized Thumbnail images and repeat steps 5 to 6
    additional_thumbnails_count = product_page.get_additional_thumbnails_count()
    if additional_thumbnails_count > 0:
        # Click the first normal-sized additional thumbnail
        product_page.click_additional_thumbnail(UIIndexes.FIRST_ADDITIONAL_THUMBNAIL)
        
        # Validate ER-4: Light box view should be displayed again
        expect(lightbox).to_be_visible()
        
        # Navigate through the images again
        product_page.click_lightbox_next()
        product_page.click_lightbox_prev()
        
        # Step 6 variation: Press 'ESC' keyboard key
        product_page.press_escape_key()
        
        # Validate ER-4: Light box view should close and focus goes to Product Display Page
        expect(lightbox).to_be_hidden()
