import pytest
from playwright.sync_api import expect,Page

# Test data
login_test_data = [
    ("laura.taylor1234@example.com", "test123", "valid"),
    ("invaliduser@example.com", "test321", "invalid"),
    ("validuser@example.com", "testxyz", "invalid"),
    ("", "", "invalid")
]

@pytest.mark.parametrize("email, password, validity", login_test_data)
def test_login_data_driven(email, password, validity,page:Page):

        page.goto("https://demowebshop.tricentis.com/login")

        # Fill login form
        page.locator("#Email").fill(email)
        page.locator("#Password").fill(password)
        page.locator('input[value="Log in"]').click()

        if validity.lower() == "valid":
            # Assert logout link visible (successful login)
            logout_link = page.locator('a[href="/logout"]')
            expect(logout_link).to_be_visible(timeout=5000)
        else:
            # Assert error message is visible (invalid login)
            error_message = page.locator(".validation-summary-errors")
            expect(error_message).to_be_visible(timeout=5000)

            # Assert user remains on login page
            expect(page).to_have_url("https://demowebshop.tricentis.com/login")
