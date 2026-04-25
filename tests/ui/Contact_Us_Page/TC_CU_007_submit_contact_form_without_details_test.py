import pytest

from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.regression
def test_submit_contact_form_without_details(page):
    """
    TC_CU_007
    (TS_027) Contact Us

    Validate submitting the Contact Form
    by not providing any details

    Preconditions:
    1. Open the Application URL
    2. User is not logged in

    Steps:
    1. Click on Phone icon option from header options
    2. Do not enter any fields in Contact Form
    3. Click Submit button (Validate ER-1)
    """

    home_page = HomePage(page)

    # Step 1: Open Contact Us page
    contact_page = home_page.navigate_to_contact_us_from_phone_icon()

    # Step 2 + Step 3: Submit empty form
    contact_page.submit_empty_contact_form()

    # Validate ER-1
    contact_page.verify_all_mandatory_fields_validation()
