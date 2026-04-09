def test_example(page):
    page.goto("https://example.com")
    assert "Example" in page.title()
