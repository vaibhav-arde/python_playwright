# pages/base_page.py
# =====================
# Base Page class that all page objects inherit from.
# Provides reusable UI interaction methods following
# the Page Object Model (POM) pattern.

import logging

from playwright.sync_api import Page, Locator

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all Page Objects. Provides common UI interaction methods."""

    def __init__(self, page: Page):
        """Initialize with a Playwright Page instance."""
        self.page = page

    def get_locator(self, locator: str | Locator) -> Locator:
        """Robustly returns a Locator. Only converts if the input is strictly a string."""
        if isinstance(locator, str):
            return self.page.locator(locator)
        return locator

    def open(self, path: str = "/"):
        """Navigate to a path relative to the current base URL."""
        self.page.goto(path)
        logger.info(f"Navigated to: {path}")

    def click(self, locator: str | Locator):
        """Click an element. Accepts string selector OR Locator object."""
        target = self.get_locator(locator)
        target.click()
        logger.info(f"Clicked: {target}")

    def fill(self, locator: str | Locator, value: str):
        """Fill a text field. Accepts string selector OR Locator object."""
        target = self.get_locator(locator)
        target.fill(value)
        logger.info(f"Filled {target} with value: {value}")

    def check(self, locator: str | Locator):
        """Select a checkbox or radio button."""
        target = self.get_locator(locator)
        target.check()
        logger.info(f"Checked element: {target}")

    def uncheck(self, locator: str | Locator):
        """Deselect a checkbox."""
        target = self.get_locator(locator)
        target.uncheck()
        logger.info(f"Unchecked element: {target}")

    def select_option(self, locator: str | Locator, **kwargs):
        """Select an option from a dropdown."""
        target = self.get_locator(locator)
        target.select_option(**kwargs)
        logger.info(f"Selected option in {target} with args: {kwargs}")

    def is_visible(self, locator: str | Locator) -> bool:
        """Check if an element is visible on the page."""
        return self.get_locator(locator).is_visible()

    def is_enabled(self, locator: str | Locator) -> bool:
        """Check if an element is enabled."""
        return self.get_locator(locator).is_enabled()

    def get_text(self, locator: str | Locator) -> str:
        """Get the inner text of an element."""
        return self.get_locator(locator).inner_text()

    def wait_for(self, locator: str | Locator, state: str = "visible", timeout: int = 10000):
        """Wait for an element to reach a specific state."""
        target = self.get_locator(locator)
        target.wait_for(state=state, timeout=timeout)
        logger.info(f"Element {target} reached state: {state}")

    def get_title(self) -> str:
        """Return the page title."""
        return self.page.title()

    def get_url(self) -> str:
        """Return the current page URL."""
        return self.page.url

    def get_warning(self, field_id: str) -> Locator:
        """Return the .text-danger warning element adjacent to a field by its ID."""
        return self.page.locator(f'#{field_id} + .text-danger')
