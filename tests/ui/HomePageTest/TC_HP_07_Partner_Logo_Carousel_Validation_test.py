"""TC_HP_007 "(TS_011) Home Page"
Validate Partner Carousel section and its slider options in the Home page
1. Open the Application URL
2. Check the Partner Carousel Logo images and slider options on the displayed Home page
(Validate ER-1, ER-2, ER-3, ER-4 and ER-5)
"""

import pytest
from pages.home_page import HomePage


@pytest.mark.ui
def test_partner_carousel(page):
    home_page = HomePage(page)

    home_page.verify_partner_carousel_section()
