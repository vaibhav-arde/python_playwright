# tests/ui/Contact_Us_Page/TC_CU_004_contact_us_fields_display_test.py

import pytest

from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.regression
def test_contact_us_required_fields_displayed(page):
    """
    TC_CU_004
    (TS_027) Contact Us

    Validate whether the required details and fields
    are displayed in the Contact Us page

    Steps:
    1. Click on Phone icon from header options
    2. Verify Contact Us page opens
    3. Validate required details and fields displayed
    """

    home_page = HomePage(page)

    # Step 1: Navigate using Phone icon
    contact_page = home_page.navigate_to_contact_us_from_phone_icon()

    # Step 2: Verify Contact Us page opened
    contact_page.verify_contact_page_opened()

    # Step 3: Validate required details and fields
    contact_page.verify_contact_details_and_fields_displayed()
