from functools import wraps
from flask import session, redirect, url_for, abort


def login_required(view_func):
    """
    로그인 여부를 검사하는 데코레이터

    - 세션에 user_id가 없으면 로그인 페이지로 이동
    - 로그인된 경우 원래 요청한 뷰 실행
    """

    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return view_func(*args, **kwargs)

    return wrapped_view


def admin_required(view_func):
    """
    관리자 여부를 검사하는 데코레이터

    - 세션에 user_id가 없으면 로그인 페이지로 이동
    - 로그인된 경우 원래 요청한 뷰 실행
    """
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        
        if session.get("auth_level") != "admin":
            abort(403)
        return view_func(*args, **kwargs)
    return wrapped