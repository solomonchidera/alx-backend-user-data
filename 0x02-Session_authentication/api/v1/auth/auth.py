#!/usr/bin/env python3
"""
0x02-Session_authentication
"""
from typing import List, TypeVar
from flask import request
import os


class Auth:
    """A class where to practice authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """A method that checks if authentication is required for a path."""
        if path and excluded_paths:
            for p in excluded_paths:
                if p.endswith('*') and path.startswith(p[:-1]):
                    return False
                elif p in {path, path + '/'}:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """A method that extract header from the request."""
        return (
            None
            if not request or "Authorization" not in request.headers
            else request.headers["Authorization"]
        )

    def current_user(self, request=None) -> TypeVar("User"):
        """A method that gets the user from the request."""
        return None

    def session_cookie(self, request=None):
        """A method that returns a cookie value from request."""
        if request is None:
            return None
        session_name = os.environ.get('SESSION_NAME')
        return request.cookies.get(session_name)
