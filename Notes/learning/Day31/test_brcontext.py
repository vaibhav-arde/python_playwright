from playwright.sync_api import Playwright, expect

# Browser--> context---> page/s


def test_browsercontext(playwright: Playwright):
    # chromium=playwright.chromium
    # browser=chromium.launch()

    browser = playwright.chromium.launch(headless=False)  # created browser
    context = browser.new_context()  # created context

    page1 = context.new_page()  # created page1
    page2 = context.new_page()  # created page2

    page1.goto("https://playwright.dev/")
    page1.wait_for_timeout(3000)
    expect(page1).to_have_title(
        "Fast and reliable end-to-end testing for modern web apps | Playwright"
    )

    page2.goto("https://www.selenium.dev/")
    page2.wait_for_timeout(3000)
    expect(page2).to_have_title("Selenium")
