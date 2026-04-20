# utils/config.py
# =====================
# Centralized environment-based configuration.
# Reads environment variables to determine the target environment
# and provides all configuration values in one place.

import os
from collections.abc import Callable
from typing import Any, TypedDict

# Active environment: set via ENV variable, defaults to "qa"
ENV = os.getenv("ENV", "qa")

# Base URLs for UI testing (keyed by environment)
BASE_URL = {
    "qa": "https://tutorialsninja.com/demo/",
    "prod": "https://tutorialsninja.com/demo/",
}

# API base URLs (keyed by environment)
API_URL = {
    "qa": "https://tutorialsninja.com/demo/index.php?route=api",
    "prod": "https://tutorialsninja.com/demo/index.php?route=api",
}


class Config:
    """Centralized test data and credentials configuration."""

    # Valid credentials
    email = "vitthalpatil5656@gmail.com"
    password = "sourabh123"

    # Invalid credentials (for negative tests)
    invalid_email = "pavanol123@abc.com"
    invalid_password = "test@123xyz"

    # Product test data
    product_name = "iMac"
    invalid_product_name = "Fitbit"
    product_quantity = "2"
    total_price = "$1,204.00"
    multiple_products_search_term = "Mac"
    correct_category = "Mac"
    parent_category = "Desktops"
    wrong_category = "PC"
    product_limit = "25"


class Product:
    def __init__(self, description_term, expected_product):
        self.description_term = description_term
        self.expected_product = expected_product


class ProductData:
    IMAC = Product("iLife", "iMac")


class SortOption(TypedDict):
    getter: Callable[[Any], Any]
    reverse: bool


SORT_CONFIG: dict[str, SortOption] = {
    "Name (A - Z)": {
        "getter": lambda page: page.get_product_names(),
        "reverse": False,
    },
    "Price (Low > High)": {
        "getter": lambda page: page.get_product_prices(),
        "reverse": False,
    },
}
