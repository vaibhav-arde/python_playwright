"""
TC_HP_010 "(TS_011) Home Page"

Validate the 'Home' page functionality in all the supported environments

1. Open the Application URL in any supported browser
2. Check the 'Home' page functionality in all the supported environments
   (Validate ER-1)

Expected Result:
User should be able to access and use the Home page correctly
in all supported browsers/environments.
"""

import pytest

from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.cross_browser
@pytest.mark.critical
def test_home_page_cross_browser_compatibility(page, base_url):
    """
    Verify Home page functionality works correctly
    across supported environments.
    """

    # Step 1: Open Application URL
    page.goto(base_url)

    # Create Page Object
    home_page = HomePage(page)

    # Step 2: Validate Home Page UI + Functionality
    home_page.verify_logo_visible()
    home_page.verify_search_bar_visible()
    home_page.verify_main_menu_visible()
    home_page.verify_slider_is_visible()
    home_page.verify_featured_section_visible()
    home_page.verify_footer_visible()