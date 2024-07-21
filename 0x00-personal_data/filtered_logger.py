#!/usr/bin/env python3
"""Module for filtering sensitive information
from log messages and database operations."""

import os
import mysql.connector
from mysql.connector import connection


def get_db() -> connection.MySQLConnection:
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
