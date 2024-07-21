#!/usr/bin/env python3
"""
Route module for the API
"""
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS
from api.v1.auth.auth import Auth
from api.v1.auth.session_db_auth import SessionDBAuth

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_type = getenv("AUTH_TYPE")
if auth_type == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth_type == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif auth_type == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif auth_type == "session_db_auth":
    auth = SessionDBAuth()


@app.before_request
def before_request():
    """Filter each request before it's handled"""
    if auth:
        exclude_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/']
        if not auth.require_auth(request.path, exclude_paths):
            return
        if not auth.authorization_header(
                request) and not auth.session_cookie(request):
            return jsonify({"error": "Unauthorized"}), 401
        current_user = auth.current_user(request)
        if current_user is None:
            return jsonify({"error": "Forbidden"}), 403
        request.current_user = current_user


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=int(port), threaded=True)
