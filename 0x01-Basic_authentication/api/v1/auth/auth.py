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
            True if path requires authentication, else False
        """
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        # Ensure path ends with '/' for consistent comparison
        path = path.rstrip('/') + '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False

        return True

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
