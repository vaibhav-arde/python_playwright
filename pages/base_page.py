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
        logger.info(f"Navigating to: {path}")
        self.page.goto(path)

    def click(self, locator: str | Locator):
        """Click an element. Accepts string selector OR Locator object."""
        target = self.get_locator(locator)
        logger.info(f"Clicking: {target}")
        target.click()

    def fill(self, locator: str | Locator, value: str):
        """Fill a text field. Accepts string selector OR Locator object."""
        target = self.get_locator(locator)
        logger.info(f"Filling element with value")
        target.fill(value)

    def check(self, locator: str | Locator):
        """Select a checkbox or radio button."""
        target = self.get_locator(locator)
        logger.info(f"Checking element")
        target.check()

    def uncheck(self, locator: str | Locator):
        """Deselect a checkbox."""
        target = self.get_locator(locator)
        logger.info(f"Unchecking element")
        target.uncheck()

    def select_option(self, locator: str | Locator, **kwargs):
        """Select an option from a dropdown."""
        target = self.get_locator(locator)
        logger.info(f"Selecting option in element")
        target.select_option(**kwargs)

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
        logger.info(f"Waiting for element to be {state}")
        target.wait_for(state=state, timeout=timeout)

    def get_title(self) -> str:
        """Return the page title."""
        return self.page.title()

    def get_url(self) -> str:
        """Return the current page URL."""
        return self.page.url
