from playwright.sync_api import Page, expect


def test_url(page: Page):
    page.goto("https://www.demoblaze.com/index.html")
    expect(page).to_have_url("https://www.demoblaze.com/index.html")


def test_Title(page: Page):
    page.goto("https://www.demoblaze.com/index.html")
    expect(page).to_have_title("STORE")


def test_google_search(page):
    page.goto("https://www.google.com")
    expect(page).to_have_title("Google")


def test_bing_search(page):
    page.goto("https://www.bing.com/")
    expect(page).to_have_title("Bing123")  # Intensionally failed
