#!/usr/bin/env python3
"""Auth class for the API authentication"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class to manage API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines whether a given path requires authentication or not
        Args:
            path (str): Url path to be checked
            excluded_paths (List[str]): List of paths
                        that don't need authentication
        Returns:
            True if path is not in excluded_paths, else False
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header from a request object
        Args:
            request: Flask request object
        Returns:
            None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns a User instance from information from a request object
        Args:
            request: Flask request object
        Returns:
            None
        """
        return None
