import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.config import Config
from utils import messages


@pytest.mark.ui
def test_validate_the_copying_of_the_text_entered_into_the_Password_field(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    # 1. Click on 'My Account' Dropmenu and navigate to Login page
    home_page.click_my_account()
    home_page.click_login()

    # 2. Enter config password into the 'Password' field
    login_page.get_password_field().fill(Config.password)

    # 3. Select the text entered into the 'Password' field via mouse, right click to select 'Copy' option (ER-1)
    login_page.select_password_text_using_mouse()
    login_page.right_click_password_field()

    # Acceptance Criteria: Copy option in the Right click menu should be disabled
    # Playwright cannot physically interact with or inspect native OS context menus.
    # To fulfill this Acceptance Criteria programmatically, we inject JavaScript to verify
    # that the browser natively flags the 'copy' command as unsupported or blocked for this field.
    is_copy_allowed = login_page.is_copy_allowed_from_password_field()
    assert not is_copy_allowed, messages.COPY_OPTION_DISABLED_MESSAGE

    # 4. Select the text entered into the 'Password' field and press (Ctrl+C) shortcut for copying (ER-2)
    login_page.select_password_text_using_keyboard()
    login_page.copy_password_text_using_keyboard()

    # 5. To verify the text was not copied by any means, try to paste it into the Email field
    login_page.get_email_field().focus()
    login_page.get_email_field().fill("")
    page.keyboard.press(messages.PASTE_SHORTCUT)

    # 6. Acceptance Criteria: Password text should not be copied.
    # Native browser behavior disables copying from password fields.
    # If a paste occurs, it will contain whatever was previously in the clipboard, never the password itself.
    expect(login_page.get_email_field()).not_to_have_value(Config.password)
