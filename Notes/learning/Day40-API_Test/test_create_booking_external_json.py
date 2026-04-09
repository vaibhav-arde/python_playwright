import json
from pathlib import Path

from playwright.sync_api import Playwright

# -------------------------------------------------------------------
# Test: Create Booking (POST request with static body)
# Request Type: POST
# Data : External json file
# -------------------------------------------------------------------


def test_create_booking(playwright: Playwright):
    base_url = "https://restful-booker.herokuapp.com"

    request_context = playwright.request.new_context()

    # Load request body from external JSON file
    file_path = Path(__file__).parent / "testdata" / "post_request_body.json"
    with open(file_path) as file:
        request_body = json.load(file)

    # Send POST request
    response = request_context.post(f"{base_url}/booking", data=request_body)

    # Extract response body
    response_body = response.json()
    print(response_body)

    # ------------------------------
    # Validations
    # ------------------------------
    assert response.ok
    assert response.status == 200

    # Validate top-level keys
    assert "bookingid" in response_body
    assert "booking" in response_body

    booking = response_body["booking"]

    # Validate booking details
    assert booking["firstname"] == "Jim"
    assert booking["lastname"] == "Brown"
    assert booking["totalprice"] == 1000
    assert booking["depositpaid"] is True
    assert booking["additionalneeds"] == "super bowls"

    # Validate booking dates (nested JSON object)
    assert booking["bookingdates"]["checkin"] == "2025-07-01"
    assert booking["bookingdates"]["checkout"] == "2025-07-05"

    # Close the API context
    request_context.dispose()
