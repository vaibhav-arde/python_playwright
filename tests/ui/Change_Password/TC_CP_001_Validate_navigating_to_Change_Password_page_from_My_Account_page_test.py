import pytest
from playwright.sync_api import expect

from pages.my_account_page import MyAccountPage
from utils.change_password_constants import CHANGE_PASSWORD_PAGE_TITLE


@pytest.mark.ui
def test_validate_navigating_to_change_password_page_from_my_account(authenticated_page):
    """
    Test Case: TC_CP_001 - Validate navigating to Change Password page from My Account page
    """
    page = authenticated_page
    my_account_page = MyAccountPage(page)

    # 3. Click on 'Change your password' link on the displayed 'My Account' page
    my_account_page.click_change_password_link()

    # 4. Acceptance Criteria - User should be navigated to 'Change Password' page
    expect(page).to_have_title(CHANGE_PASSWORD_PAGE_TITLE)
