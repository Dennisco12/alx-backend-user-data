#!/usr/bin/env python3
"""End to end integration test
"""

import requests
import json

EMAIL = "guillaume@holberton.io7"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """register user test
    """
    payload = {"email": email, "password": password}
    r = requests.post('http://0.0.0.0:5000/users', data=payload)
    print(r.text)
    # r = r.text
    resp = json.dumps({"email":email,"message":"user created"})
    print(resp)
    assert r.json() == resp
    #assert r['email'] == email
    #assert r['message'] == "user created"


if __name__ == '__main__':
    register_user(EMAIL, PASSWD)
