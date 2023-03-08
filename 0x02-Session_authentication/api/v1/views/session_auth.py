#!/usr/bin/env python3

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ This handles user log in
    """
    email = request.form.get("email", None)
    password = request.form.get("password", None)

    if not email or email == "":
        return jsonify({ "error": "email missing" }), 400
    if not password or password == "":
        return jsonify({ "error": "password missing" }), 400

    user_list = User.search({"email": email})
    if len(user_list) == 0:
        return jsonify({ "error": "no user found for this email" }), 404

    for user in user_list:
        if not user.is_valid_password(password):
            return jsonify({ "error": "wrong password" }), 401
        else:
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            session = getenv('SESSION_NAME')
            msg = jsonify(user.to_json())
            msg.set_cookie(session, session_id)
            return msg

@app_views.route('/auth_session/logout', strict_slashes=False,
                 methods=['DELETE'])
def logout():
    """ This logs out a user from the session
    """
    from api.v1.app import auth
    des = auth.destroy_session(request)
    if des is False:
        abort(404)
    return jsonify({}), 200
