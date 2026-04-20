"""TC_HP_009 "(TS_011) Home Page"
Validate the UI of 'Home' page functionality
1. Open the Application URL in any supported browser
2. Check the UI of the functionality related to 'Home' page
"""

import pytest
from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.smoke
def test_home_page_ui(page, base_url):
    page.goto(base_url)

    home_page = HomePage(page)

    # UI Validations
    home_page.verify_home_page_ui()
