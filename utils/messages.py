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
WARN_PASSWORD_MISMATCH = "Password confirmation does not match password!"
WARN_EMAIL_ALREADY_EXISTS = "Warning: E-Mail Address is already registered!"

# ===== Product Comparison =====
COMPARISON_PAGE_TITLE = "Product Comparison"
COMPARISON_PAGE_HEADING = "Product Comparison"
COMPARE_BUTTON_TOOLTIP = "Compare this Product"
COMPARE_SUCCESS = "Success: You have added {product_name} to your product comparison!"

# ===== Login Field error message =====
WARN_LOGIN_ERROR = "Warning: No match for E-Mail Address and/or Password."

ACCOUNT_PAGE_TITLE = "My Account"
FORGOT_PASSWORD = "Forgotten Password"
LOGIN_PAGE_TITLE = "Account Login"
FORGOT_PASSWORD_PAGE_TITLE = "Forgot Your Password?"
CHANGE_PASSWORD_PAGE_TITLE = "Change Password"
EMAIL_PLACEHOLDER = "E-Mail Address"
PASSWORD_PLACEHOLDER = "Password"
WARN_LOGIN_ATTEMPTS_EXCEEDED = "Warning: Your account has exceeded allowed number of login attempts. Please try again in 1 hour."
SUCCESS_PASSWORD_UPDATED = "Success: Your password has been successfully updated."
EMPTY_COMPARISON_MESSAGE = "You have not chosen any products to compare."
ADD_TO_CART_SUCCESS = "Success: You have added {product_name} to your shopping cart!"
ERR_PRODUCT_NOT_FOUND_IN_COMPARISON = "Product '{product_name}' not found in comparison table."
REMOVE_SUCCESS = "Success: You have modified your product comparison!"

# ===== Comparison Table UI Checklist =====
COMPARISON_TABLE_HEADERS = [
    "Product",
    "Image",
    "Price",
    "Model",
    "Brand",
    "Availability",
    "Rating",
    "Summary",
    "Weight",
    "Dimensions (L x W x H)",
]

# Change Password Field error message
WARN_PASSWORD_MISMATCH = "Password confirmation does not match password!"
WARN_PASSWORD_REQUIRED = "Password must be between 4 and 20 characters!"


# Change Password Field assert message
ASSERT_PASSWORD_REQUIRED = "Password field should be marked as mandatory with a red asterisk"
ASSERT_PASSWORD_CONFIRM_REQUIRED = (
    "Password Confirm field should be marked as mandatory with a red asterisk"
)
