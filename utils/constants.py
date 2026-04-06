# utils/constants.py
# =====================

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
    REGISTER = "/index.php?route=account/register"
    MY_ACCOUNT = "/index.php?route=account/account"
    LOGOUT = "/index.php?route=account/logout"
    SEARCH = "/index.php?route=product/search"
    CART = "/index.php?route=checkout/cart"
    CHECKOUT = "/index.php?route=checkout/checkout"


# =====================
# UI Attributes
# =====================

class UIAttributes:
    """Common UI attribute names"""

    PLACEHOLDER = "placeholder"
    VALUE = "value"
    TYPE = "type"
    CLASS = "class"
    ID = "id"
    NAME = "name"


# =====================
# Register Page Constants
# =====================

class RegisterPlaceholders:
    """Register Page Placeholder values"""

    FIRST_NAME = "First Name"
    LAST_NAME = "Last Name"
    EMAIL = "E-Mail"
    TELEPHONE = "Telephone"
    PASSWORD = "Password"
    CONFIRM_PASSWORD = "Password Confirm"
