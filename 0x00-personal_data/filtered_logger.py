#!/usr/bin/env python3
"""Module for filtering sensitive information from log messages."""

import logging
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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record, redacting specified fields."""
        record.msg = filter_datum(
            self.fields,
            self.REDACTION,
            record.getMessage(),
            self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
