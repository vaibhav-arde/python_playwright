'''
capture screenshots, videos and trace for the test
'''

from playwright.sync_api import Page, expect
import pytest

def test_url(page: Page):
    page.goto('https://www.demoblaze.com/index.html')
    expect(page).to_have_url("https://www.demoblaze.com/index.html1")


def test_Title(page: Page):
    page.goto('https://www.demoblaze.com/index.html')
    expect(page).to_have_title("STORE")


def test_Login(page: Page):
    page.goto('https://www.demoblaze.com/index.html')
    page.locator('#login2').click()
    page.locator('#loginusername').fill('pavanol')
    page.locator('#loginpassword').fill('test@123')
    page.locator("button:has-text('Log in')").click()
    page.wait_for_timeout(3000)
    expect(page.locator("#logout2")).to_be_visible()
    expect(page.locator('#nameofuser')).to_contain_text('Welcome pavanol')
