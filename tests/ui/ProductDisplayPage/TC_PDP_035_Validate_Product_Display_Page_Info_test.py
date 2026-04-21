"""TC_PDP_035	"(TS_007)
Product Display Page"	Validate Page Title, Page Heading and Page URL of the 'Product Display' page
1. Enter any existing Product name into the Search text box field  - <Refer Test Data>
2. Click on the button having search icon
3. Click on the Product displayed in the Search results
4. Check the Page Title, Page Heading and Page URL of hte displayed 'Product Display' page (Validate ER-1)"	"Product Name: iMac
"""

# ==========================================================
# File:
# tests/ui/ProductDisplayPageTest/
# TC_PDP_035_validate_page_title_heading_url_test.py
# ==========================================================

import re
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from utils.config import Config


@pytest.mark.ui
@pytest.mark.regression
def test_validate_page_title_heading_url_of_product_display_page(page):
    """
    Validate Page Title, Page Heading and Page URL
    of the Product Display Page.
    """

    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)
    product_page = ProductPage(page)

    product_name = Config.imac_product

    # Step 1: Search Product
    home_page.enter_product_name(product_name)
    home_page.click_search()

    # Step 2: Select Product from Search Results
    search_results_page.select_product(product_name)

    # Step 3: Validate Page Heading
    expect(product_page.get_page_heading()).to_have_text(product_name)

    # Step 4: Validate Page Title
    expect(page).to_have_title(re.compile(product_name))

    # Step 5: Validate Page URL
    expect(page).to_have_url(re.compile("product"))
