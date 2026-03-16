"""
Pre-requisites:
----------------
Install dependencies
    pip install jsonschema

"""
from jsonschema import validate, ValidationError
from playwright.sync_api import sync_playwright, Playwright

# Helper function to validate schema
def validate_json_schema(response_json,myschema):
    try:
        validate(instance=response_json,schema=myschema)
        print("Schema validation succcessfull..")
        return True
    except ValidationError as e:
        print("Schema validation failed")
        return False



def test_validate_json_schema(playwright:Playwright):
    request_context = playwright.request.new_context()

    response=request_context.get("https://jsonplaceholder.typicode.com/posts/1")

    assert response.ok
    response_body=response.json()

    print(response_body)

    # schema ( Generated from teh tool https://transform.tools/json-to-json-schema)
    schema = {
        "title": "Generated schema for Root",
        "type": "object",
        "properties": {
            "userId": {
                "type": "number"
            },
            "id": {
                "type": "number"
            },
            "title": {
                "type": "string"
            },
            "body": {
                "type": "string"
            }
        },
        "required": [
            "userId",
            "id",
            "title",
            "body"
        ]
    }

    is_valid=validate_json_schema(response_body,schema)
    assert is_valid

    request_context.dispose()


