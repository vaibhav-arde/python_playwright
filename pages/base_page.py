# pages/base_page.py
# =====================
# Base Page class that all page objects inherit from.
# Provides reusable UI interaction methods following
# the Page Object Model (POM) pattern.

import logging

from playwright.sync_api import Page

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all Page Objects. Provides common UI interaction methods."""

    def __init__(self, page: Page):
        """Initialize with a Playwright Page instance."""
        self.page = page

    def open(self, path: str = "/"):
        """Navigate to a path relative to the current base URL."""
        logger.info(f"Navigating to: {path}")
        self.page.goto(path)

    def click(self, locator: str):
        """Click an element identified by a CSS/XPath selector string."""
        logger.info(f"Clicking: {locator}")
        self.page.locator(locator).click()

    def fill(self, locator: str, value: str):
        """Fill a text input identified by a CSS/XPath selector string."""
        logger.info(f"Filling '{locator}' with value")
        self.page.locator(locator).fill(value)

    def get_text(self, locator: str) -> str:
        """Get the inner text of an element."""
        return self.page.locator(locator).inner_text()

    def is_visible(self, locator: str) -> bool:
        """Check if an element is visible on the page."""
        return self.page.locator(locator).is_visible()

    def wait_for(self, locator: str, state: str = "visible", timeout: int = 10000):
        """Wait for an element to reach a specific state."""
        logger.info(f"Waiting for '{locator}' to be {state}")
        self.page.locator(locator).wait_for(state=state, timeout=timeout)

    def get_title(self) -> str:
        """Return the page title."""
        return self.page.title()

    def get_url(self) -> str:
        """Return the current page URL."""
        return self.page.url

    def get_element_attribute(self, element, attribute_name: str):
        """
        Return the value of a given attribute from a locator.

        Args:
            element: Playwright locator
            attribute_name (str): HTML attribute name

        Returns:
            str | None: Attribute value if present, else None
        """
        return element.get_attribute(attribute_name)
