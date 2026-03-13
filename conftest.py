import pytest
from datetime import datetime
from pathlib import Path
from slugify import slugify
import allure

def pytest_configure(config):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    config.option.htmlpath = f"reports/report_{timestamp}.html"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    screen_file = ''
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call":
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            if "page" in item.funcargs:
                page = item.funcargs["page"]
                screenshot_dir = Path("screenshots")
                screenshot_dir.mkdir(exist_ok=True)
                screen_file = str(screenshot_dir / f"{slugify(item.nodeid)}.png")
                page.screenshot(path=screen_file)

                # add the screenshots to the html report
                extra.append(pytest_html.extras.png(screen_file))

                # Attach to Allure report
                allure.attach.file(
                    screen_file,
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )

        report.extra = extra