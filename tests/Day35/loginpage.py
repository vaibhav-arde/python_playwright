from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.login_link = page.locator("#login2")
        self.username_input = page.locator("#loginusername")
        self.password_input = page.locator("#loginpassword")
        self.login_button = page.locator("button[onclick='logIn()']")

    # Action methods
    def click_login_link(self):
        self.login_link.click()

    def enter_username(self, username):
        self.username_input.fill("")  # Clear before entering
        self.username_input.fill(username)

    def enter_password(self, password):
        self.password_input.fill("")  # Clear before entering
        self.password_input.fill(password)

    def click_login_button(self):
        self.login_button.click()

    def perform_login(self, username, password):
        self.click_login_link()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
