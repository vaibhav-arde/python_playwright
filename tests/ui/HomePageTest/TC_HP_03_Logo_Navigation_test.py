"""TC_HP_003	"(TS_011)

Home Page"	Validate navigating to Home page from any page of the Applcation using Logo
1. Open the Application URL and navigate to any page of the Application
1. Click on the Logo 'Your Store' in our application (Validate ER-1)	Not Applicable
1. User should be taken to Home page"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from utils.constants import UIRoutes, expected_title


@pytest.mark.ui
def test_logo_navigation(page, base_url):
    home_page = HomePage(page)

    # Step 1: Navigate to another page
    page.goto(base_url + UIRoutes.LOGIN)

    # Step 2: Click logo
    home_page.click_logo()

    # Step 3: Validate title
    expect(page).to_have_title(expected_title)
