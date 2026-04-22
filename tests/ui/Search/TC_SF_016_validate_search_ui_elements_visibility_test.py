"""
Test Case ID: #59
Test Case Description: Validate 'Search' textbox field and the button having search icon are displayed on all the pages of the Application

1. Navigate to various key pages of the Application (Validate ER-1)
"""

from pages.header_page import HeaderComponent
import pytest
from playwright.sync_api import expect
from utils.constants import UIRoutes


@pytest.mark.ui
@pytest.mark.parametrize(
    "route",
    [
        UIRoutes.HOME,
        UIRoutes.LOGIN,
        UIRoutes.REGISTER,
        UIRoutes.CART,
        UIRoutes.CHECKOUT,
        UIRoutes.SEARCH,
    ],
)
def test_search_ui_elements_visibility(page, route):
    header_page = HeaderComponent(page)
    header_page.open(route)

    expect(header_page.get_search_box()).to_be_visible()
    expect(header_page.get_search_button()).to_be_visible()
