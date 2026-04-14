from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(base_url="https://tutorialsninja.com/demo/")
        page = context.new_page()
        
        # Search for iMac
        page.goto("/")
        page.fill('input[name="search"]', "iMac")
        page.click('button.btn-default.btn-lg')
        
        # Select iMac
        page.click('h4 > a:has-text("iMac")')
        
        # Add to cart
        page.fill('input[name="quantity"]', "2")
        page.click('#button-cart')
        
        # Wait for alert
        try:
            # Try multiple selectors
            selectors = [
                "div.alert.alert-success.alert-dismissible",
                "div.alert-success",
                ".alert-success",
                "div.alert"
            ]
            for selector in selectors:
                loc = page.locator(selector)
                if loc.count() > 0:
                    print(f"Found with selector: {selector}")
                    print(f"Text: {loc.first.inner_text()}")
                    break
            else:
                print("No success alert found!")
                
        except Exception as e:
            print(f"Error: {e}")
            
        page.wait_for_timeout(2000)
        browser.close()

if __name__ == "__main__":
    run()
