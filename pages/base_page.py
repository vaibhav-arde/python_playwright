# pages/base_page.py
# =====================

import re
import logging
from playwright.sync_api import Page, Locator

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all Page Objects. Provides common UI interaction methods."""

    def __init__(self, page: Page):
        self.page = page

        # Common Locator
        self.img_logo = page.locator("#logo a")

    def get_locator(self, locator: str | Locator) -> Locator:
        if isinstance(locator, str):
            return self.page.locator(locator)
        return locator

    def open(self, path: str = "/"):
        self.page.goto(path)
        logger.info(f"Navigated to: {path}")

    def click(self, locator: str | Locator):
        target = self.get_locator(locator)
        target.click()
        logger.info(f"Clicked: {target}")

    def fill(self, locator: str | Locator, value: str):
        target = self.get_locator(locator)
        target.fill(value)
        logger.info(f"Filled {target} with value: {value}")

    def check(self, locator: str | Locator):
        target = self.get_locator(locator)
        target.check()
        logger.info(f"Checked element: {target}")

    def uncheck(self, locator: str | Locator):
        target = self.get_locator(locator)
        target.uncheck()
        logger.info(f"Unchecked element: {target}")

    def select_option(self, locator: str | Locator, **kwargs):
        target = self.get_locator(locator)
        target.select_option(**kwargs)
        logger.info(f"Selected option in {target} with args: {kwargs}")

    def is_visible(self, locator: str | Locator) -> bool:
        return self.get_locator(locator).is_visible()

    def is_enabled(self, locator: str | Locator) -> bool:
        return self.get_locator(locator).is_enabled()

    def get_text(self, locator: str | Locator) -> str:
        return self.get_locator(locator).inner_text()

    def wait_for(self, locator: str | Locator, state: str = "visible", timeout: int = 10000):
        target = self.get_locator(locator)
        target.wait_for(state=state, timeout=timeout)
        logger.info(f"Element {target} reached state: {state}")

    def tab_until_focused(self, locator: str | Locator, max_tabs: int = 50):
        """Press Tab until the specified locator is focused."""
        target = self.get_locator(locator)
        for _ in range(max_tabs):
            if target.and_(self.page.locator(":focus")).count() > 0:
                logger.info(f"Element {target} is now focused")
                return
            self.page.keyboard.press("Tab")
        raise RuntimeError(f"Could not reach {target} using Tab after {max_tabs} attempts.")

    def get_title(self) -> str:
        return self.page.title()

    def get_url(self) -> str:
        return self.page.url

    def verify_url(self, expected_url: str | re.Pattern):
        """Verify the current page URL matches the expected URL (supports regex)."""
        expect(self.page).to_have_url(expected_url)
        logger.info(f"Verified URL matches: {expected_url}")

    def get_warning(self, field_id: str) -> Locator:
        return self.page.locator(f"#{field_id} + .text-danger")

    # ✅ FIXED: No import here
    def click_logo(self):
        """Click on the site logo."""
        self.click(self.img_logo)
        logger.info("Clicked on Logo (Your Store)")