#!/usr/bin/env python3
"""
0x00-personal_data
"""
import re
import os
import mysql.connector
from typing import List
import logging

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """A function that returns the log message obfuscated."""
    for field in fields:
        pattern = rf"{field}=\S+?(?={re.escape(separator)}|$)"
        message = re.sub(pattern, f"{field}={redaction}", message)
    return message


def get_logger() -> logging.Logger:
    """A function that returns a logging.Logger object."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """A function that returns a connector to the database."""
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")
    conn = mysql.connector.connect(
        user=db_username, password=db_password, host=db_host, database=db_name
    )
    return conn


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """The method init of the class."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """A method that filters incoming log records."""
        return filter_datum(
            self.fields, self.REDACTION, super().format(record), self.SEPARATOR
        )


def main() -> None:
    """The main function."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    logger = get_logger()
    redaction = logger.handlers[0].formatter.REDACTION
    for row in cursor.fetchall():
        name, email, phone, ssn, password, ip, last_login, user_agent = row
        formatted_row = (
            f"name={redaction}; email={redaction}; phone={redaction}; "
            f"ssn={redaction}; password={redaction}; ip={ip}; "
            f"last_login={last_login}; user_agent={user_agent}"
        )
        logger.info(formatted_row)
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
