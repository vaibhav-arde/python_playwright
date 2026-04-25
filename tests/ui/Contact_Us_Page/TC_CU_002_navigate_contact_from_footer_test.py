import pytest

from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.regression
def test_navigate_contact_us_from_footer(page, base_url):
    """
    TC_CU_002
    (TS_027) Contact Us

    Validate navigating to Contact Us page
    from Footer options
    """

    home_page = HomePage(page)

    # Step 1: Navigate from footer
    contact_page = home_page.navigate_to_contact_us_from_footer()

    # Step 2: Validate page opened
    contact_page.verify_contact_page_opened()

    # Step 3: Validate URL
    assert "contact" in page.url.lower()
