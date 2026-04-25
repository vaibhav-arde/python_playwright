# tests/ui/Contact_Us_Page/TC_CU_013_contact_us_cross_browser_test.py

import pytest

from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.cross_browser
def test_contact_us_cross_browser(page):
    """
    TC_CU_013
    (TS_027) Contact Us

    Validate the Contact Us page functionality
    in all the supported environments

    Preconditions:
    1. Open the Application URL

    Steps:
    1. Check the Contact Us page functionality
       in all the supported environments
       (Validate ER-1)
    """

    home_page = HomePage(page)

    # Open Contact Us page
    contact_page = home_page.navigate_to_contact_us_from_phone_icon()

    # Validate ER-1
    contact_page.verify_contact_us_page_functionality()
