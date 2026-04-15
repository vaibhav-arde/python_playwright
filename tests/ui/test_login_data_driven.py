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

# Filter data for success and failure scenarios to ensure declarative tests
success_data = [row for row in excel_data if row[3] == "success"]
failure_data = [row for row in excel_data if row[3] != "success"]


@pytest.mark.datadriven
@pytest.mark.parametrize("testName,email,password,expected", success_data)
def test_login_success_data_driven(page, testName, email, password, expected):
    """Verify successful login with valid credentials."""
    home_page = HomePage(page)
    login_page = LoginPage(page)
    my_account_page = MyAccountPage(page)

    home_page.click_my_account()
    home_page.click_login()

    login_page.login(email, password)

    expect(my_account_page.get_my_account_page_heading()).to_be_visible(timeout=5000)


@pytest.mark.datadriven
@pytest.mark.parametrize("testName,email,password,expected", failure_data)
def test_login_failure_data_driven(page, testName, email, password, expected):
    """Verify login failure with invalid credentials."""
    home_page = HomePage(page)
    login_page = LoginPage(page)

    home_page.click_my_account()
    home_page.click_login()

    login_page.login(email, password)

    expect(login_page.get_login_error()).to_be_visible(timeout=5000)
