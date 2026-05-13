from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://tutorialsninja.com/demo/")
    try:
        print("Waiting for My Account...")
        page.locator("a[title='My Account']").wait_for(state="visible", timeout=10000)
        print("My Account is visible!")
        page.locator("a[title='My Account']").click()
        print("Clicked My Account")
        page.get_by_role("link", name="Login").wait_for(state="visible", timeout=5000)
        print("Login link is visible!")
    except Exception as e:
        print(f"Error: {e}")
        page.screenshot(path="scratch/fail_my_account.png")
    browser.close()
