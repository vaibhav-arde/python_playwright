# tests/ui/Contact_Us_Page/TC_CU_008_invalid_email_contact_form_test.py

import pytest

from pages.home_page import HomePage
from utils.constants import InvalidEmail


@pytest.mark.ui
@pytest.mark.regression
def test_invalid_email_contact_form(page):
    """
    TC_CU_008
    (TS_027) Contact Us

    Validate entering invalid email address into the
    E-Mail Address field and submit the form

    Preconditions:
    1. Open the Application URL
    2. User is not logged in

    Steps:
    1. Click on Phone icon option from header options
    2. Enter valid details into Your Name and Enquiry fields
    3. Enter invalid email address into E-Mail Address field
    4. Click Submit button (Validate ER-1)
    """

    email = InvalidEmail.test_data[0][0]

    home_page = HomePage(page)

    contact_page = home_page.navigate_to_contact_us_from_phone_icon()

    contact_page.submit_contact_form_with_invalid_email(email)

    contact_page.verify_invalid_email_validation()
