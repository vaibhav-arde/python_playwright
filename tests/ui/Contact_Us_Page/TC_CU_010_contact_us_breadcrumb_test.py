# tests/ui/Contact_Us_Page/TC_CU_010_contact_us_breadcrumb_test.py

import pytest

from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.regression
def test_contact_us_breadcrumb(authenticated_page):
    """
    TC_CU_010
    (TS_027) Contact Us

    Validate the Breadcrumb of Contact Us page

    Preconditions:
    1. Open the Application URL and login

    Steps:
    1. Click on Phone icon option from header options
    2. Check the Breadcrumb of the displayed
       Contact Us page (Validate ER-1)
    """

    home_page = HomePage(authenticated_page)

    # Step 1: Open Contact Us page
    contact_page = home_page.navigate_to_contact_us_from_phone_icon()

    # Step 2: Validate breadcrumb
    contact_page.verify_contact_us_breadcrumb()
