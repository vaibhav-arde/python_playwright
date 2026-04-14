# utils/constants.py
# =====================
# Centralized constants for API endpoints and HTTP headers.
# Avoids hardcoding values across tests and API clients.


class APIEndpoints:
    """Centralized API endpoint paths."""

    BASE = "/index.php?route=api"
    LOGIN = f"{BASE}/login"
    CART = f"{BASE}/cart"
    COUPON = f"{BASE}/coupon"
    ORDER = f"{BASE}/order"
    PAYMENT = f"{BASE}/payment"
    SHIPPING = f"{BASE}/shipping"


class Headers:
    """Common HTTP request headers."""

    JSON = {
        "Content-Type": "application/json",
    }

    FORM = {
        "Content-Type": "application/x-www-form-urlencoded",
    }


class UIRoutes:
    """Common UI route paths (relative to base URL)."""

    HOME = "/"
    LOGIN = "/index.php?route=account/login"
    REGISTER = "index.php?route=account/register"
    MY_ACCOUNT = "/index.php?route=account/account"
    LOGOUT = "/index.php?route=account/logout"
    SEARCH = "/index.php?route=product/search"
    CART = "/index.php?route=checkout/cart"
    CHECKOUT = "/index.php?route=checkout/checkout"


class UserDetails:
    """User details for validate existing account in registration."""

    first_name = "Pavan"
    last_name = "B"
    email = "pavanoltraining@gmail.com"
    telephone = "814240XXXX"
    password = "12345"
    confirm_password = "12345"


class InvalidPassword:
    password = "12345"
    confirm_password = "abcde"


class InvalidEmail:
    """Invalid email test data and expected Chromium validation tooltips."""

    test_data = [
        ("pavanol", "Please include an '@' in the email address."),
        ("pavanol@", "Please enter a part following '@'."),
        ("@gmail.com", "Please enter a part followed by '@'."),
    ]


INVALID_PHONE_NUMBERS = [
    "1",  # too short
    "12",  # too short
    "abcde",  # non-numeric (BUG case)
    "123abc",  # mixed input (BUG case)
    "@@@@",  # special chars (BUG case)
    "123456789012345678901234567890123",  # too long
]


class UILabels:
    # UI Page Headings
    REGISTER_PAGE_HEADING = "Register Account"
    REGISTER_BREADCRUMB = "Register"

class UITitles:
    REGISTER_PAGE_TITLE = "Register Account"

class TestData:
    # Test Data
    VALID_PASSWORD = "Test@123"
    INVALID_PASSWORD = "123"

    PRODUCT_NAME_IMAC = "iMac"
    
