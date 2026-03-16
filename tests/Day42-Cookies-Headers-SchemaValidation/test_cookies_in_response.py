from playwright.sync_api import Playwright


def test_cookies_in_response(playwright:Playwright):
    request_context=playwright.request.new_context()

    response=request_context.get("https://www.google.com/")

    assert response.status_text=="OK"   #assert response.ok
    assert response.status==200

    # Extract all teh cookies from the response
    cookies=request_context.storage_state()["cookies"]

    for c in cookies:
        print(f"{c['name']}==>{c['value']}==>{c['domain']}")


    # Check if 'AEC' cookie is exist
    aec_cookie= None

    for c in cookies:
        if c["name"] =="AEC":
            aec_cookie=c
            break

    assert aec_cookie is not None, "Cookie 'AEC' not found"

    # Printing details of 'AEC' Cookie

    print(aec_cookie['name'])
    print(aec_cookie['value'])
    print(aec_cookie['domain'])
    print(aec_cookie['path'])
    print(aec_cookie['expires'])




