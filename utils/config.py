# utils/config.py
# =====================
# Centralized environment-based configuration.
# Reads environment variables to determine the target environment
# and provides all configuration values in one place.

import os

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
    product_name = "MacBook"
    product_quantity = "2"
    total_price = "$1,204.00"
