"""
로그인 상태 확인용 데코레이터
"""

from functools import wraps
from flask import session, redirect, url_for


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
