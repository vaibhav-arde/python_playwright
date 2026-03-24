import openpyxl
import json
import time
from playwright.sync_api import sync_playwright

email = f"testuser_{int(time.time())}@abc.com"
password = "test@123"

def register_user():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://tutorialsninja.com/demo/index.php?route=account/register")
        page.fill("#input-firstname", "Test")
        page.fill("#input-lastname", "User")
        page.fill("#input-email", email)
        page.fill("#input-telephone", "1234567890")
        page.fill("#input-password", password)
        page.fill("#input-confirm", password)
        page.check("input[name='agree']")
        page.click("input[value='Continue']")
        page.wait_for_selector("h1:text('Your Account Has Been Created!')", timeout=10000)
        print("Successfully registered:", email)
        browser.close()

def update_config():
    with open("utils/config.py", "r") as f:
        content = f.read()
    content = content.replace('email = "pavanol@abc.com"', f'email = "{email}"')
    with open("utils/config.py", "w") as f:
        f.write(content)

def update_json():
    with open("test_data/logindata.json", "r") as f:
        data = json.load(f)
    for row in data:
        if row["expected"] == "success":
            row["email"] = email
    with open("test_data/logindata.json", "w") as f:
        json.dump(data, f, indent=2)

def update_excel():
    wb = openpyxl.load_workbook("test_data/logindata.xlsx")
    sheet = wb.active
    # Find the row with "success" and update it
    for row in sheet.iter_rows(min_row=2):
        if row[3].value == "success":
            row[1].value = email
    wb.save("test_data/logindata.xlsx")

if __name__ == "__main__":
    print("Registering new user...")
    register_user()
    print("Updating configuration...")
    update_config()
    update_json()
    update_excel()
    print("Done!")
