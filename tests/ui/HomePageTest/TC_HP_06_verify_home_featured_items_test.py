"""TC_HP_006 "(TS_011) Home Page"
Validate four featured products should be displayed in the Home Page
1. Open the Application URL
2. Check the Featured section in the displayed Home page (Validate ER-1 and ER-2)"""

import pytest

from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.regression
def test_verify_four_featured_products(page):
    home_page = HomePage(page)

    home_page.verify_featured_section_visible()
    home_page.verify_four_featured_products()
