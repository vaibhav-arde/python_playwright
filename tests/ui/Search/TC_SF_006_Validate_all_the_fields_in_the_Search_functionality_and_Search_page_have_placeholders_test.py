"""
Test Case ID: #39
Description: Validate all the fields in the Search functionality and Search page have placeholders

1.Don't enter anything into the 'Search' text box field
2.Click on the button having search icon (Validate ER-1)

expected result
1. Proper placeholder text is displayed in the below fields:
- Search text box field
- Search Criteria text box field


"""

import pytest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.assertions import validate_placeholder


@pytest.mark.ui
def test_search_page_have_placeholders(page):
    home_page = HomePage(page)
    search_results_page = SearchResultsPage(page)

    # Validate Home page search box placeholder
    validate_placeholder(home_page.get_search_box())

    home_page.click_search()

    # Validate Search result page search criteria placeholder
    validate_placeholder(search_results_page.get_search_criteria_textbox())
