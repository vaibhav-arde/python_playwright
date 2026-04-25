# tests/ui/Contact_Us_Page/TC_CU_001_navigate_contact_us_page_test.py
"""
TC_CU_001
(TS_027) Contact Us

Validate navigating to Contact Us page
from Header options

Steps:
1. Open the Application URL
2. Click on Contact Us option from header
3. Verify Contact Us page is opened
"""

import pytest

from pages.home_page import HomePage


@pytest.mark.ui
def test_navigate_contact_us_page(page, base_url):
    home_page = HomePage(page)

    # Step 2: Navigate to Contact Us page
    contact_page = home_page.navigate_to_contact_us_page()

    # Step 3: Validate Contact Us page opened
    contact_page.verify_contact_page_opened()

    # Step 4: Validate URL
    assert "contact" in page.url.lower()
