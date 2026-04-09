from playwright.sync_api import Page


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        # CSS selector targeting all product links under the product cards
        self.products_list_locator = "div#tbodyid div.card h4.card-title a"
        # 'Add to cart' button (exact match using text)
        self.add_to_cart_button = page.locator('//a[text()="Add to cart"]')
        # Cart link in the top menu
        self.cart_link = page.locator("#cartur")

    def add_product_to_cart(self, product_name: str):
        products = self.page.locator(self.products_list_locator)
        count = products.count()

        for i in range(count):
            name = products.nth(i).text_content().strip()
            if name == product_name:
                products.nth(i).click()
                break

        self.page.on("dialog", lambda dialog: dialog.accept())  # handle dialog
        self.add_to_cart_button.click()

    def goto_cart(self):
        self.cart_link.click()
