#!/usr/bin/env python3
"""A flask app"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
Auth = Auth()


@app.route('/')
def index():
    """Index route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """This creates a new user
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        Auth.register_user(email, password)
        return jsonify({"email": email,
                        "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """This logs a user into the app
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if Auth.valid_login(email, password) is False:
        abort(401)
    session_id = Auth.create_session(email)
    payload = jsonify({"email": email, "message": "logged in"})
    payload.set_cookie("session_id", session_id)
    return payload


@app.route('/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """This destroy a user's session
    """
    session_id = request.headers.get("session_id")
    user = Auth.get_user_from_session_id(session_id)
    Auth.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', strict_slashes=False)
def profile():
    """This retrieves a user profile based on session_id
    """
    session_id = request.cookies.get("session_id")
    user = Auth.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route('/reset_password', strict_slashes=False, methods=['POST'])
def get_reset_password_token():
    """This generates a token and respond with 200 code
    """
    email = request.form.get("email")
    try:
        token = Auth.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', strict_slashes=False, methods=['PUT'])
def reset_password():
    """This reset the user password
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        Auth.update_password(reset_token, new_password)
        return jsonify({'email': email, 'message': 'password updated'}), 200
    except ValueError:
        abort(403)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
