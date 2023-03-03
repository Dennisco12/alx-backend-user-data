#!/usr/bin/env python3
"""This encrypts a user password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """This returns a salted, hashed password which is a
    byte string"""
    password = password.encode()
    return bcrypt.hashpw(password, bcrypt.gensalt())


def is_valid(hashed_password: bytes,
             password: str) -> bool:
    """returns true if password matches hash_password"""
    password = password.encode()
    return bcrypt.checkpw(password, hashed_password)
