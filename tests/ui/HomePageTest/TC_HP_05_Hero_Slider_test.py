# tests/ui/HomePageTest/TC_HP_005_Hero_Slider_test.py
# ==========================================================
# Test Case: TC_HP_005 - Hero Slider Functionality
# Validate Hero Images and slider options on Home Page
# ==========================================================

import pytest
from pages.home_page import HomePage


@pytest.mark.ui
def test_hero_slider_functionality(page, base_url):
    """
    TC_HP_005 (TS_011) Home Page
    Validate Hero Images and its slider options in the Home page.
    """

    # Open Application
    page.goto(base_url)

    home_page = HomePage(page)

    # Step 1: Hero slider visible
    home_page.verify_slider_is_visible()

    # Step 2: At least one image available
    home_page.verify_slider_images_present()

    # Step 3: Navigation buttons visible (if present)
    home_page.verify_navigation_buttons_are_visible()

    # Step 4: Next button changes image
    initial_img_src = home_page.get_active_image_src()
    home_page.click_slider_next()
    home_page.verify_image_changed(initial_img_src)

    # Step 5: Pagination dots visible
    home_page.verify_pagination_is_visible()

    # Step 6: Prev button changes image again
    current_img_src = home_page.get_active_image_src()
    home_page.click_slider_prev()
    home_page.verify_image_changed(current_img_src)