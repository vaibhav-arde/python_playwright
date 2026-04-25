# tests/ui/Contact_Us_Page/TC_CU_009_submit_contact_form_after_login_test.py

import pytest

from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.regression
def test_submit_contact_form_after_login(authenticated_page):
    """
    TC_CU_009
    (TS_027) Contact Us

    Validate submitting the Contact Form
    in Contact Us page by providing all
    the details after login

    Preconditions:
    1. Open the Application URL
    2. User is logged in

    Steps:
    1. Click on Phone icon option from header options (Validate ER-1)
    2. Enter any text into Enquiry field
    3. Click on Submit button (Validate ER-2)
    4. Click on Continue button (Validate ER-3)
    """

    home_page = HomePage(authenticated_page)

    # Step 1: Open Contact Us page
    contact_page = home_page.navigate_to_contact_us_from_phone_icon()

    # Validate ER-1
    contact_page.verify_contact_page_opened()

    # Step 2 + Step 3
    contact_page.submit_contact_form_after_login()

    # Validate ER-2
    contact_page.verify_success_message_visible()

    # Step 4
    contact_page.click_continue()

    # Validate ER-3
    assert "common/home" in authenticated_page.url.lower()
