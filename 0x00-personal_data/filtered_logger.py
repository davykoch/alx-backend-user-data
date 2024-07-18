#!/usr/bin/env python3
"""Module for filtering sensitive information from log messages."""

import re
from typing import List


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """Obfuscates specified fields in the log message."""
    return re.sub(
        f'({"|".join(fields)})=[^{separator}]*',
        f'\\1={redaction}',
        message)
