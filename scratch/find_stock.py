from playwright.sync_api import sync_playwright

def find_instock():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('https://tutorialsninja.com/demo/index.php?route=product/search&search=%20')
        products = page.locator('#content h4 > a').all()
        found = []
        for i in range(len(products)):
            pr = page.locator('#content h4 > a').nth(i)
            name = pr.inner_text()
            pr.click()
            page.wait_for_load_state('load')
            try:
                status = page.locator('li:has-text("Availability:")').inner_text()
                if 'In Stock' in status:
                    # Check if it has required options
                    if page.locator('#product .form-group.required').count() == 0:
                        print(f"FOUND_INSTOCK_NO_OPTIONS: {name}")
                        found.append(name)
                    else:
                        print(f"FOUND_INSTOCK_WITH_OPTIONS: {name}")
            except:
                pass
            page.go_back()
            if len(found) >= 3:
                break
        browser.close()

if __name__ == "__main__":
    find_instock()
