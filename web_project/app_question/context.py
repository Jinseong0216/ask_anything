# app_question/context.py
from flask import session

def inject_globals():
    return {
        "current_user": {
            "id": session.get("user_id"),
            "name": session.get("user_name"),
            "role": session.get("role"),
            "auth_level": session.get("auth_level"),
        },
        "is_login": "user_id" in session,
        "is_admin": session.get("auth_level") == "admin",
    }
