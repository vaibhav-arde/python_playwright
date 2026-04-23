from playwright.sync_api import expect
import pytest
from pages.my_account_page import MyAccountPage
from pages.logout_page import LogoutPage
from pages.login_page import LoginPage


@pytest.mark.ui
def test_logout_all_devices(authenticated_page, new_context, auth_state_path):
    # 🔹 Device 1 (Existing authenticated browser context from pytest)
    page1 = authenticated_page
    base_url = page1.url.split("index.php")[0]
    my_account_page_1 = MyAccountPage(page1)

    # Step 1: Navigate to 'My Account' to Verify user is logged in (Device 1)
    my_account_page_1.open_my_account_page(base_url)
    expect(page1).to_have_title(my_account_page_1.get_expected_title())

    # 🔹 Device 2 (Simulating a second device/context using the same active session)
    # Using the same storage_state accurately duplicates the logged-in user tokens
    context2 = new_context(storage_state=auth_state_path)
    page2 = context2.new_page()
    my_account_page_2 = MyAccountPage(page2)

    # Step 2: Verify user logged in successfully on Device 2
    my_account_page_2.open_my_account_page(base_url)
    expect(page2).to_have_title(my_account_page_2.get_expected_title())

    # -------------------------------
    # Step 3: Logout from Device 1
    # -------------------------------
    my_account_page_1.click_my_account_dropdown()
    my_account_page_1.click_logout()

    # Optional checking to ensure Device 1 hit the logout page successfully
    logout_page_1 = LogoutPage(page1)
    expect(logout_page_1.verify_logout_page_heading()).to_be_visible()

    # -------------------------------
    # Step 4: Try accessing a protected page (Address Book) in Device 2
    # -------------------------------

    # Because Device 1 invalidated the session stored on the server, Device 2's session
    # cookie is now officially obsolete and should be securely rejected by the server backend.
    my_account_page_2.open_address_book_page(base_url)

    # Validating the Login Page UI specifically loaded to request new credentials
    login_page_2 = LoginPage(page2)
    expect(page2).to_have_title(login_page_2.get_title())
    expect(login_page_2.verify_login_btn_visible()).to_be_visible()

    # Cleanup Device 2 context explicitly
    context2.close()
