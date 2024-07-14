#!/usr/bin/env python3
""" Module of session views
"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
from os import getenv


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def session_login() -> str:
    """POST /api/v1/auth_session/login
    Return:
      - A route for the user authentication.
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]
    if not user.is_valid_password(str(password)):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    session_name = getenv("SESSION_NAME")
    response = jsonify(user.to_json())
    response.set_cookie(session_name, session_id)
    return response


@app_views.route("/auth_session/logout",
                 methods=["DELETE"],
                 strict_slashes=False)
def session_logout() -> str:
    """POST /api/v1/auth_session/logout
    Return:
      - A route for the user logout.
    """
    from api.v1.app import auth

    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
