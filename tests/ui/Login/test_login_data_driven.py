"""
Test Case: Data-Driven Login Functionality

Uses test data from Excel file to run login tests with multiple
credential sets (valid and invalid).
"""

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from utils.data_loader import read_excel_data

# Load/read the data from the test data files
excel_data = read_excel_data("test_data/logindata.xlsx")


@pytest.mark.datadriven
@pytest.mark.parametrize("testName,email,password,expected", excel_data)
def test_login_data_driven(page, testName, email, password, expected):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    my_account_page = MyAccountPage(page)

    home_page.click_my_account()
    home_page.click_login()

    login_page.login(email, password)

    if expected == "success":
        expect(my_account_page.get_my_account_page_heading()).to_be_visible(
            timeout=5000
        )
    else:
        expect(login_page.get_login_error()).to_be_visible(timeout=5000)
