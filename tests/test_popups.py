from playwright.sync_api import sync_playwright, expect, Playwright

def test_hande_popups(playwright:Playwright):
    browser=playwright.chromium.launch(headless=False)
    context=browser.new_context()
    page=context.new_page()

    page.goto("https://testautomationpractice.blogspot.com/")

    # def handle_popup(popup):
    #     popup.wait_for_load_state()
    #
    # page.on("popup",handle_popup)

    page.on("popup",lambda popup:popup.wait_for_load_state())

    page.locator("#PopUp").click()

    page.wait_for_timeout(5000)

    all_popups=context.pages
    print("Total number of popups/pages:",len(all_popups))

    # capture urls of all teh popup pages
    for pw in all_popups:
        print("Popup/Page URL======>", pw.url)
        title=pw.title()
        if "Playwright" in title:
            pw.locator(".getStarted_Sjon").click()
            pw.wait_for_timeout(3000)
            expect(pw).to_have_title("Installation | Playwright")
            pw.close() # close the playwright popup/window

    page.wait_for_timeout(5000)
    context.close()
    browser.close()















