import pytest

from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.regression
def test_contact_us_ui_validation(page):
    """
    TC_CU_012
    (TS_027) Contact Us

    Validate the UI of Contact Us page functionality

    Preconditions:
    1. Open the Application URL

    Steps:
    1. Check the UI of functionality related to
       Contact Us page (Validate ER-1)
    """

    home_page = HomePage(page)

    # Open Contact Us page
    contact_page = home_page.navigate_to_contact_us_from_phone_icon()

    # Validate ER-1
    contact_page.verify_contact_us_page_ui()
