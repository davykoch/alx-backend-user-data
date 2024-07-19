#!/usr/bin/env python3
"""
Session Authentication views module
This module handles routes for session-based authentication
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from api.v1.app import auth
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Handles user login and session creation

    Returns:
        - JSON representation of the user if login is successful
        - Error message with appropriate status code if login fails
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    session_name = os.getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)
    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """
    Handles user logout by destroying the session

    Returns:
        - Empty JSON dictionary with status code 200 if logout is successful
        - 404 error if session destruction fails
    """
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
