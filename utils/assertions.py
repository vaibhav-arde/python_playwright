from playwright.sync_api import expect


def assert_products_match_search(products, search_term):
    count = products.count()
    assert count > 1, f"Expected multiple products, got {count}"

    expect(products.first).to_be_visible()

    for i in range(count):
        expect(products.nth(i)).to_contain_text(search_term, ignore_case=True)
