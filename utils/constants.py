# utils/constants.py
# =====================
# Centralized constants for API endpoints and HTTP headers.
# Avoids hardcoding values across tests and API clients.


class APIEndpoints:
    """Centralized API endpoint paths."""

    BASE: str = "/index.php?route=api"
    LOGIN: str = f"{BASE}/login"
    CART: str = f"{BASE}/cart"
    COUPON: str = f"{BASE}/coupon"
    ORDER: str = f"{BASE}/order"
    PAYMENT: str = f"{BASE}/payment"
    SHIPPING: str = f"{BASE}/shipping"


class Headers:
    """Common HTTP request headers."""

    JSON: dict[str, str] = {
        "Content-Type": "application/json",
    }

    FORM: dict[str, str] = {
        "Content-Type": "application/x-www-form-urlencoded",
    }


class UIRoutes:
    """Common UI route paths (relative to base URL)."""

    HOME: str = "/"
    LOGIN: str = "/index.php?route=account/login"
    REGISTER: str = "index.php?route=account/register"
    MY_ACCOUNT: str = "/index.php?route=account/account"
    LOGOUT: str = "/index.php?route=account/logout"
    SEARCH: str = "/index.php?route=product/search"
    CART: str = "/index.php?route=checkout/cart"
    CHECKOUT: str = "/index.php?route=checkout/checkout"


class UserDetails:
    """User details for validate existing account in registration."""

    first_name: str = "Pavan"
    last_name: str = "B"
    email: str = "pavanoltraining@gmail.com"
    telephone: str = "814240XXXX"
    password: str = "12345"
    confirm_password: str = "12345"


class InvalidPassword:
    password: str = "12345"
    confirm_password: str = "abcde"


class InvalidEmail:
    """Invalid email test data and expected Chromium validation tooltips."""

    test_data: list[tuple[str, str]] = [
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
