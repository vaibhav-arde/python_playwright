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

# ===== Login Field error message =====
WARN_LOGIN_ERROR = "Warning: No match for E-Mail Address and/or Password."

ACCOUNT_PAGE_TITLE = "My Account"
FORGOT_PASSWORD = "Forgotten Password"
LOGIN_PAGE_TITLE = "Account Login"
FORGOT_PASSWORD_PAGE_TITLE = "Forgot Your Password?"
EMAIL_PLACEHOLDER = "E-Mail Address"
PASSWORD_PLACEHOLDER = "Password"
WARN_LOGIN_ATTEMPTS_EXCEEDED = "Warning: Your account has exceeded allowed number of login attempts. Please try again in 1 hour."
SUCCESS_PASSWORD_UPDATED = "Success: Your password has been successfully updated."

# Aliases for compatibility with older test files
INVALID_LOGIN_MSG = WARN_LOGIN_ERROR
PRIVACY_POLICY_WARNING_MSG = WARN_PRIVACY_POLICY
SUCCESS_REGISTER_MSG = ACCOUNT_CREATED

# ===== Product Display Page / Cart Messages =====
SUCCESS_ALERT_KEYWORD = "Success"
WARNING_ALERT_KEYWORD = "Warning"
INVALID_QTY_ALERT_EXPECTATION = "Expected success or warning alert for invalid quantity input"
AVAILABILITY_STATUS_EMPTY = "Availability status should not be empty"
AVAILABILITY_STATUS_UNEXPECTED = "Unexpected availability status: '{status}'"
SEARCH_RESULT_PRODUCT_NOT_FOUND = "No product found in search results for '{keyword}'"
SEARCH_RESULT_PRODUCT_NAME_EMPTY = "Product Name in search results should not be empty"
PDP_PRODUCT_NAME_MISMATCH = "Expected Product Name '{expected}', but got '{actual}'"
PDP_PRODUCT_BRAND_EMPTY = "Product Brand should not be empty"
PDP_PRODUCT_CODE_EMPTY = "Product Code should not be empty"
THUMBNAIL_SRC_SHOULD_CHANGE_ON_NEXT = "Lightbox image source should change after clicking next"
