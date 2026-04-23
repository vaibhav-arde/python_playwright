from playwright.sync_api import expect
import pytest
from pages.my_account_page import MyAccountPage


@pytest.mark.ui
def test_user_session_persistence(authenticated_page, new_context, auth_state_path):

    page = authenticated_page
    base_url = page.url.split("?")[0]

    # 1: Navigate to account page
    my_account_page = MyAccountPage(page)

    my_account_page.open_my_account_page(base_url)

    # 2: Verify user logged in
    expect(page).to_have_title(my_account_page.get_expected_title())

    my_account_page.click_my_account_dropdown()

    expect(my_account_page.verify_logout_btn_in_dropdown()).to_be_visible()

    # 3: Close the browser context
    page.context.close()

    # 4: Reopen browser
    reopened_context = new_context(storage_state=auth_state_path)
    new_page = reopened_context.new_page()

    new_my_account_page = MyAccountPage(new_page)
    new_my_account_page.open_my_account_page(base_url)

    # 5: Verify session(user still logged in by verifying page title)
    expect(new_page).to_have_title(new_my_account_page.get_expected_title())

    new_my_account_page.click_my_account_dropdown()

    expect(new_my_account_page.verify_logout_btn_in_dropdown()).to_be_visible()
