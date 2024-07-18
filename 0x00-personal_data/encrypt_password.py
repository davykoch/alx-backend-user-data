#!/usr/bin/env python3
"""Module for hashing passwords and validating hashed passwords"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: A salted, hashed password.
    """
    # Convert the password string to bytes
    password_bytes = password.encode('utf-8')

    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates a password against a hashed password.

    Args:
        hashed_password (bytes): The hashed password to compare against.
        password (str): The password to validate.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    # Convert the password string to bytes
    password_bytes = password.encode('utf-8')

    # Use bcrypt to check if the password matches the hashed password
    return bcrypt.checkpw(password_bytes, hashed_password)
