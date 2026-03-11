import pytest

from playwright.sync_api import expect,Playwright

# Test data
search_items = ['laptop', 'Gift card', 'smartphone', 'monitor']

@pytest.mark.parametrize("item", search_items)
def test_search_items(item, page):
    page.goto("https://demowebshop.tricentis.com/")

    # Fill search box and click search button
    page.locator("#small-searchterms").fill(item)
    page.locator("input[value='Search']").click()

    # Assertion: first result title should contain the search item
    first_result = page.locator("h2 a").nth(0)
    expect(first_result).to_contain_text(item, ignore_case=True)
