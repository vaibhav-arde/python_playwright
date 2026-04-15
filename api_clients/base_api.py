# api_clients/base_api.py
# =====================
# Base API client class providing reusable HTTP method wrappers.
# All API client classes should inherit from this base.

import logging
from typing import Any
from playwright.sync_api import APIRequestContext, APIResponse

logger = logging.getLogger(__name__)


class BaseAPI:
    """Base class for all API clients. Wraps Playwright's APIRequestContext."""

    def __init__(self, request: APIRequestContext, headers: dict[str, str] | None = None) -> None:
        """
        Initialize the API client.

        :param request: Playwright APIRequestContext instance
        :param headers: Optional default headers for all requests
        """
        self.request = request
        self.headers = headers or {}

    def get(self, endpoint: str, **kwargs: Any) -> APIResponse:
        """Send a GET request."""
        logger.info(f"GET {endpoint}")
        return self.request.get(endpoint, headers=self.headers, **kwargs)

    def post(self, endpoint: str, **kwargs: Any) -> APIResponse:
        """Send a POST request."""
        logger.info(f"POST {endpoint}")
        return self.request.post(endpoint, headers=self.headers, **kwargs)

    def put(self, endpoint: str, **kwargs: Any) -> APIResponse:
        """Send a PUT request."""
        logger.info(f"PUT {endpoint}")
        return self.request.put(endpoint, headers=self.headers, **kwargs)

    def patch(self, endpoint: str, **kwargs: Any) -> APIResponse:
        """Send a PATCH request."""
        logger.info(f"PATCH {endpoint}")
        return self.request.patch(endpoint, headers=self.headers, **kwargs)

    def delete(self, endpoint: str, **kwargs: Any) -> APIResponse:
        """Send a DELETE request."""
        logger.info(f"DELETE {endpoint}")
        return self.request.delete(endpoint, headers=self.headers, **kwargs)
