#!/usr/bin/env python3
"""This filters out some fields from a message"""
from typing import List
import re
import logging
import os
import mysql.connector

PII_FIELDS = ("name", "email", "ssn", "phone", "password")


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """This takes a message and returns a redacted message"""
    msgList = message.split(separator)
    for msg in msgList:
        if msg.split("=")[0] in fields:
            message = re.sub(msg.split("=")[1], redaction, message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """This filters values in incoming log records"""
        msg = super(RedactingFormatter, self).format(record)
        msg = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return msg


def get_logger() -> logging.Logger:
    """This returns a logging.Logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """This creates a connection to a database"""
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', "root")
    pwd = os.getenv('PERSONAL_DATA_DB_PASSWORD', "")
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db = os.getenv('PERSONAL_DATA_DB_NAME')
    return mysql.connector.connect(
            user=user,
            host=host,
            passwd=pwd,
            port=3306,
            db=db)


def main():
    """This displays the data from the database in a redacted format"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    logger = get_logger()
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    for row in rows:
        record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, row),
            )
        msg = '{};'.format('; '.join(list(record)))
        # print(msg)
        log_record = logging.LogRecord("user_data", logging.INFO, None,
                                        None, msg, None, None)
        formatter = RedactingFormatter(PII_FIELDS)
        formatter.FORMAT = "[HOLBERTON] user_data %(levelname)s %(asctime)-15s: %(message)s"
        # logger.handle(formatter.format(log_record))
        print(formatter.format(log_record))
    cursor.close()
    db.close()


if __name__ == '__main__':
    main2()
