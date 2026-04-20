import glob

'''
shortcut script to automatically replace code in many files.
This script will refactor the test files to use the get_text() method instead of text_content()
'''

def refactor():
    base_dir = r"C:\Projects\Python_Fremework_Playwright\python_playwright\tests\ui"

    for file_path in glob.glob(f"{base_dir}\\**\\*.py", recursive=True):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        new_content = content.replace(
            "product_in_results.text_content()",
            "search_results_page.get_text(product_in_results)"
        )

        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(new_content)

            print(f"Updated: {file_path}")


if __name__ == "__main__":
    refactor()