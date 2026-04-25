# tests/ui/Contact_Us_Page/TC_CU_006_submit_contact_form_valid_details_test.py

import pytest

from pages.home_page import HomePage
from utils.constants import UserDetails


@pytest.mark.ui
@pytest.mark.regression
def test_submit_contact_form_valid_details(page):
    """
    TC_CU_006
    (TS_027) Contact Us

    Validate submitting the Contact Form in Contact Us page
    by providing all the details

    Preconditions:
    1. Open the Application URL
    2. User is not logged in

    Steps:
    1. Click on Phone icon option from header options
    2. Enter all the fields in Contact Form with valid details
    3. Click Submit button (Validate ER-1)
    4. Click Continue button (Validate ER-2)
    """

    home_page = HomePage(page)

    # Step 1: Open Contact Us page via Phone icon
    contact_page = home_page.navigate_to_contact_us_from_phone_icon()

    # Step 2 + Step 3: Submit form with valid details
    contact_page.submit_contact_form(
        UserDetails.first_name, UserDetails.email, "Need product information"
    )

    # Validate ER-1: Success page/message displayed
    contact_page.verify_success_message_visible()

    # Step 4: Click Continue button
    contact_page.click_continue()

    # Validate ER-2: Redirected successfully
    assert "common/home" in page.url.lower()
