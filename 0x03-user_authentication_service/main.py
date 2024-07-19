#!/usr/bin/env python3
"""
Main file
"""
import requests

def register_user(email: str, password: str) -> None:
    """Register a new user"""
    response = requests.post('http://127.0.0.1:5000/users', data={'email': email, 'password': password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}

def log_in_wrong_password(email: str, password: str) -> None:
    """Attempt to log in with an incorrect password"""
    response = requests.post('http://127.0.0.1:5000/sessions', data={'email': email, 'password': password})
    assert response.status_code == 401

def log_in(email: str, password: str) -> str:
    """Log in a user and return the session ID"""
    response = requests.post('http://127.0.0.1:5000/sessions', data={'email': email, 'password': password})
    assert response.status_code == 200
    assert "session_id" in response.cookies
    return response.cookies["session_id"]

def profile_unlogged() -> None:
    """Access the profile endpoint without being logged in"""
    response = requests.get('http://127.0.0.1:5000/profile')
    assert response.status_code == 403

def profile_logged(session_id: str) -> None:
    """Access the profile endpoint while logged in"""
    response = requests.get('http://127.0.0.1:5000/profile', cookies={'session_id': session_id})
    assert response.status_code == 200
    assert "email" in response.json()

def log_out(session_id: str) -> None:
    """Log out a user and destroy the session"""
    response = requests.delete('http://127.0.0.1:5000/sessions', cookies={'session_id': session_id})
    assert response.status_code == 200

def reset_password_token(email: str) -> str:
    """Get a reset password token for a user"""
    response = requests.post('http://127.0.0.1:5000/reset_password', data={'email': email})
    assert response.status_code == 200
    return response.json()["reset_token"]

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update a user's password"""
    response = requests.put('http://127.0.0.1:5000/reset_password', data={'email': email, 'reset_token': reset_token, 'new_password': new_password})
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


# Test the functions
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

 
