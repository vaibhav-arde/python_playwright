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

class Messages:
    """Common UI messages."""
    ACCOUNT_CREATED = "Your Account Has Been Created!"
    MY_ACCOUNT_HEADING = "My Account"

    # ===== Registration Field Validation Warnings =====
    WARN_FIRST_NAME = "First Name must be between 1 and 32 characters!"
    WARN_LAST_NAME = "Last Name must be between 1 and 32 characters!"
    WARN_EMAIL = "E-Mail Address does not appear to be valid!"
    WARN_TELEPHONE = "Telephone must be between 3 and 32 characters!"
    WARN_PASSWORD = "Password must be between 4 and 20 characters!"
    WARN_PRIVACY_POLICY = "Warning: You must agree to the Privacy Policy!"
