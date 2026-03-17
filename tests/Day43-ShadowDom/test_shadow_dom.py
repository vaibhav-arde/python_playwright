import time

from playwright.sync_api import Page, expect

def test_example(page: Page) :
    page.goto("https://books-pwakit.appspot.com/")
    #page.locator("#input").fill("Welcome")   # CSS

    #page.locator('book-app').getByRole('textbox', {name: 'Search Books'})
    #page.locator('book-app').get_by_role("searchbox", name='Search Books').fill("welcome") #SELECTORSHUB SUGGESTION
    page.get_by_role("searchbox", name='Search Books').fill("welcome")    #DIRECT
    time.sleep(5)
