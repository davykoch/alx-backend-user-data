#!/usr/bin/env python3
"""Module for filtering sensitive information
from log messages and database operations."""

import logging
import mysql.connector
from mysql.connector import connection
import os
import re
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """Obfuscates specified fields in the log message."""
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


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


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database."""
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    db_connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )

    return db_connection


# def main():
    #"""Main function to retrieve and display filtered user data."""

    #logger = get_logger()
    #db = get_db()
    #cursor = db.cursor()

    #cursor.execute("SELECT * FROM users;")
    #fields = [i[0] for i in cursor.description]

    # for row in cursor:
    #   message = "; ".join(
    #        f"{fields[i]}={row[i]}" for i in range(
   #             len(fields)))
  #      logger.info(message)

 #   cursor.close()
#    db.close()


# if __name__ == "__main__":
 #   main()
