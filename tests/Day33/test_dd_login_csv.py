import csv

import pytest
from playwright.sync_api import Page, expect

login_data = []  # empty list

# read csv file
csvfile = open("testdata/data.csv", newline="", encoding="utf-8")
reader = csv.DictReader(csvfile)

for row in reader:
    login_data.append((row["email"], row["password"], row["validity"]))


@pytest.mark.parametrize("email, password, validity", login_data)
def test_login_data_driven_csv(email, password, validity, page: Page):
    page.goto("https://demowebshop.tricentis.com/login")

    # fill teh login form
    page.locator("#Email").fill(email)  # email id
    page.locator("#Password").fill(password)  # password
    page.locator("input[value='Log in']").click()

    # validation
    if validity == "valid":
        logout_link = page.locator("a[href='/logout']")
        expect(logout_link).to_be_visible(timeout=5000)
    else:
        error_message = page.locator(".validation-summary-errors")
        expect(error_message).to_be_visible(timeout=5000)  # checking error message
        expect(page).to_have_url(
            "https://demowebshop.tricentis.com/login"
        )  # checking same login page
