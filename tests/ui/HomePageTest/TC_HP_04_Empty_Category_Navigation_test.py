"""TC_HP_004
"(TS_011) Home Page"
 Validate navigating to Home page from any Category Page which don't have any products
 1. Open the Application URL
 Steps:
 "1. Hover the mouse on 'Desktops' menu
 2. Select 'PC(0)' option which has zero products
 3. Click on 'Continue' button in the PC Category page having zero products displayed (Validate ER-1)"
 Not Applicable
 1. User should be taken to Home page
"""

import pytest
from playwright.sync_api import expect

from pages.category_page import CategoryPage
from pages.home_page import HomePage
from utils.constants import expected_title


@pytest.mark.ui
def test_home_navigation_from_empty_category(page):

    home_page = HomePage(page)
    home_page.navigate_to_empty_pc_category()

    category_page = CategoryPage(page)
    category_page.verify_empty_category()
    category_page.click_continue()

    expect(page).to_have_title(expected_title)
    expect(home_page.img_logo).to_be_visible()
