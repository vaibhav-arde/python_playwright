from playwright.sync_api import Page, expect


def test_Login(page: Page):
    page.goto("https://www.demoblaze.com/index.html")
    page.wait_for_timeout(5000)
    page.locator("#login2").click()
    page.locator("#loginusername").fill("pavanol")
    page.locator("#loginpassword").fill("test@123")
    page.locator("button:has-text('Log in')").click()
    page.wait_for_timeout(10000)
    expect(page.locator("#logout2")).to_be_visible()
    expect(page.locator("#nameofuser")).to_contain_text("Welcome pavanol")
