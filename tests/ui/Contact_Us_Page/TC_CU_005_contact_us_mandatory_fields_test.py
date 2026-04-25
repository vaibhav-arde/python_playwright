# tests/ui/Contact_Us_Page/TC_CU_005_contact_us_mandatory_fields_test.py

import pytest

from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.regression
def test_contact_us_mandatory_fields(page):
    """
    TC_CU_005
    (TS_027) Contact Us

    Validate all the text fields in the Contact Us page
    are mandatory

    Steps:
    1. Click on Phone icon option from header
    2. Submit form without entering values
    3. Verify mandatory validations for:
       - Your Name
       - E-Mail Address
       - Enquiry
    """

    home_page = HomePage(page)

    # Step 1: Open Contact Us page via Phone icon
    contact_page = home_page.navigate_to_contact_us_from_phone_icon()

    # Step 2: Submit empty form
    contact_page.submit_empty_contact_form()

    # Step 3: Verify all mandatory field validations
    contact_page.verify_all_mandatory_fields_validation()
