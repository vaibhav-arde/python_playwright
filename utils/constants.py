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
    WISHLIST = "/index.php?route=account/wishlist"
    COMPARE = "/index.php?route=product/compare"
    INDEX_ENTRY = "index.php"


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


class UITimeouts:
    CART_ALERT_WAIT_MS = 5000


class UIAvailability:
    VALID_PRODUCT_STATUSES = ["In Stock", "Out Of Stock", "Pre-Order", "2-3 Days"]


class UIPricing:
    CURRENCY_SYMBOLS = ["$", "\u20ac", "\u00a3"]


class UIIndexes:
    FIRST_ADDITIONAL_THUMBNAIL = 0


class UIAttributes:
    IMAGE_SOURCE = "src"


class TestData:
    # Test Data
    VALID_PASSWORD = "Test@123"
    DEFAULT_PASSWORD = "Password123"
    DEFAULT_TELEPHONE = "1234567890"
    INVALID_PASSWORD = "123"

    PRODUCT_NAME_IMAC = "iMac"
    PRODUCT_NAME_HTC = "HTC Touch HD"
    PRODUCT_NAME_MACBOOK = "MacBook"
    PRODUCT_NAME_APPLE_CINEMA_30 = 'Apple Cinema 30"'
    PRODUCTS_WITH_SPECIFICATION_TAB = [PRODUCT_NAME_APPLE_CINEMA_30, PRODUCT_NAME_MACBOOK]
    REVIEW_AUTHOR_NAME = "Automation Reviewer"
    REVIEW_TEXT_VALID = "This is an automation review submitted for test validation."
    REVIEW_RATING_VALUE = "5"
    REVIEW_TEXT_TOO_SHORT = "Short review"
    REVIEW_TEXT_TOO_LONG = "A" * 1001
    CART_TARGET_QUANTITY = "2"
    INVALID_PRODUCT_QUANTITY = "0"
    MINIMUM_PRODUCT_QUANTITY = "2"
    BELOW_MINIMUM_PRODUCT_QUANTITY = "1"
    ABOVE_MINIMUM_PRODUCT_QUANTITY = "3"
    EMPTY_VALUE = ""
    COMMA_SPACE_SEPARATOR = ", "
