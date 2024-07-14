#!/usr/bin/env python3
"""
0x02-Session_authentication
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """A class that inherits from Auth."""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """A method that returns the Base64 of the Authorization header."""
        return (
            authorization_header[6:]
            if authorization_header is not None
            and isinstance(authorization_header, str)
            and authorization_header.startswith("Basic ")
            else None
        )

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """A method that returns the decoded value of base64."""
        if base64_authorization_header is not None and isinstance(
                base64_authorization_header, str):
            try:
                decodedBytes = base64.b64decode(base64_authorization_header)
                return decodedBytes.decode('utf-8')
            except (base64.binascii.Error, UnicodeDecodeError):
                return None
        return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """A method that returns user's email & password from base64 decode."""
        if decoded_base64_authorization_header is not None and isinstance(
            decoded_base64_authorization_header, str
        ) and ':' in decoded_base64_authorization_header:
            user, password = decoded_base64_authorization_header.split(':', 1)
            return (user, password)
        return (None, None)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """A method that returns the user instance based on credentials."""
        if user_email and isinstance(
            user_email, str
        ) and user_pwd and isinstance(user_pwd, str):
            try:
                userList = User.search({'email': user_email})
            except Exception:
                return None
            for user in userList:
                if user.is_valid_password(user_pwd):
                    return user
                return None
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """A method that overloads Auth and retrieves the User instance
        for a request."""
        authHeader = self.authorization_header(request)
        extract = self.extract_base64_authorization_header(authHeader)
        decode = self.decode_base64_authorization_header(extract)
        userEmail, userPass = self.extract_user_credentials(decode)
        userObject = self.user_object_from_credentials(userEmail, userPass)
        return userObject
