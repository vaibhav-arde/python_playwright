# api_clients/user_api.py
# =====================
# API Client for user-related operations including registration and authentication.

from typing import Any
from playwright.sync_api import APIResponse
from api_clients.base_api import BaseAPI
from utils.constants import APIEndpoints


class UserAPI(BaseAPI):
    """API client for User management operations."""

    def create_user(self, user_data: dict[str, Any]) -> APIResponse:
        """
        Creates a new user account via API.

        :param user_data: Dictionary containing registration details (firstname, lastname, email, etc.)
        :return: APIResponse object
        """
        return self.post(
            APIEndpoints.LOGIN, data=user_data
        )  # Note: Using LOGIN endpoint as per current framework Constants if register is same path

    def authenticate_user(self, credentials: dict[str, str]) -> APIResponse:
        """
        Authenticates a user and returns the session/token.

        :param credentials: Dictionary containing email and password
        :return: APIResponse object
        """
        return self.post(APIEndpoints.LOGIN, data=credentials)
