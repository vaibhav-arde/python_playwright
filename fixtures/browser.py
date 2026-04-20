# fixtures/browser.py
# =====================
# Browser-related fixtures.
# This module relies on pytest-playwright's built-in browser management.
# Adds auto-navigation to base_url and screenshot-on-failure hooks.

import logging
import time
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Error as PlaywrightError

logger = logging.getLogger(__name__)
DNS_RESOLVE_ERROR = "ERR_NAME_NOT_RESOLVED"
BASE_NAV_RETRIES = 3
BASE_NAV_RETRY_DELAY_SEC = 2


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture the test result (pass/fail/skip) after each test phase.
    This is used to decide whether to take screenshots or save traces.
    """
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(scope="function", autouse=True)
def navigate_to_base_url(request, page):
    """
    Auto-navigate the page to the base URL before each test.
    pytest-playwright's page fixture starts at about:blank,
    so this ensures all tests begin at the configured base URL.
    """
    base_url = request.config.getoption("--base-url", default=None)
    if base_url:
        logger.info(f"Navigating to base URL: {base_url}")
        last_error = None
        for attempt in range(1, BASE_NAV_RETRIES + 1):
            try:
                page.goto(base_url)
                page.wait_for_load_state("load")
                
                # Handle landing page redirect if it occurs
                landing_link = page.get_by_role("link", name="https://tutorialsninja.com/demo")
                if landing_link.is_visible():
                    logger.info("Landing page detected by fixture, clicking through...")
                    landing_link.click()
                    page.wait_for_load_state("load")
                
                break
            except PlaywrightError as exc:
                last_error = exc
                error_text = str(exc)
                is_dns_error = DNS_RESOLVE_ERROR in error_text

                if not is_dns_error or attempt == BASE_NAV_RETRIES:
                    raise

                logger.warning(
                    "Base URL navigation failed due to DNS resolution "
                    f"(attempt {attempt}/{BASE_NAV_RETRIES}). Retrying in "
                    f"{BASE_NAV_RETRY_DELAY_SEC}s..."
                )
                time.sleep(BASE_NAV_RETRY_DELAY_SEC)

        if last_error:
            logger.info("Recovered from transient base URL navigation error after retry")

    yield

    # After test: check result and capture artifacts
    test_name = request.node.name
    test_failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

    if test_failed:
        logger.info(f"Test '{test_name}' FAILED — capturing artifacts")

        # Take screenshot on failure
        screenshot_dir = Path("reports/screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = str(screenshot_dir / f"{test_name}.png")

        try:
            page.screenshot(path=screenshot_path)
            logger.info(f"Screenshot saved: {screenshot_path}")

            allure.attach.file(
                screenshot_path,
                name=f"{test_name}_screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception as e:
            logger.warning(f"Could not capture screenshot: {e}")

        # Attach video if available
        try:
            video_path = page.video.path() if page.video else None
            if video_path and Path(video_path).exists():
                allure.attach.file(
                    str(video_path),
                    name=f"{test_name}_video",
                    attachment_type=allure.attachment_type.WEBM,
                )
                logger.info("Video attached to Allure report")
        except Exception as e:
            logger.warning(f"Could not attach video: {e}")
