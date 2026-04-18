import re
from playwright.sync_api import expect, Locator


def assert_products_match_search(products, search_term):
    """Validate that all displayed products match the given search term."""
    count = products.count()
    assert count > 0, f"Expected multiple products, got {count}"
    for i in range(count):
        expect(products.nth(i)).to_contain_text(search_term, ignore_case=True)


# Validates that an input field has a proper and meaningful placeholder
def validate_placeholder(locator: Locator):
    """
    Validate that an input field has a proper placeholder.

    Ensures:
    - Placeholder attribute exists (not None)
    - Placeholder is not empty or whitespace
    - Placeholder length is greater than 2 characters
    """
    value = locator.get_attribute("placeholder")

    assert value is not None
    assert value.strip()
    assert len(value.strip()) > 2


# Extracts numeric price value from text (removes symbols and formats it as float)
def extract_price(text: str) -> float:
    """Extract numerical price from text using regex."""
    clean = text.split("\n")[0].replace(",", "").replace("$", "")
    match = re.search(r"(\d+\.?\d*)", clean)
    return float(match.group(1)) if match else 0.0
