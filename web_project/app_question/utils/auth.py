from functools import wraps
from flask import session, redirect, url_for, abort

from app_question.models import User


def login_required(view_func):
    """
    def login_required(view_func):
    
    로그인 여부를 검사하는 데코레이터

    [역할]
    - 특정 view 함수 앞에 붙어서 "로그인 했는지"를 먼저 검사
    - 로그인 안 되어 있으면 로그인 페이지로 강제 이동
    - 로그인 되어 있으면 원래 view 함수를 그대로 실행

    사용 예:
        @login_required
        def home():
            ...

    이때 home()은 바로 실행되지 않고,
    login_required(home)가 먼저 호출된다.
    
    @wraps(view_func)
    wraps의 역할 (중요)
    # 없으면 생기는 문제:
    home.__name__  → 'decorated'
    url_for("main.home") 동작 이상 가능
    디버깅/로그 꼬임

    @wraps(view_func)는
    원래 함수의 이름, docstring, endpoint 정보를 보존해준다.

    Flask에서는 endpoint 이름이 함수 이름이기 때문에
    wraps 없으면 라우팅 관련 버그가 생길 수 있음

        def decorated(*args, **kwargs):
    decorated 함수란?
    Flask가 실제로 실행하는 함수

    원래 view_func를 감싸는 래퍼(wrapper)

    요청 → decorated() → 로그인 검사 → view_func() 실행
            user = get_current_user()
    현재 로그인 사용자 조회
    def get_current_user():
        if "user_id" not in session:
            return None
        return User.query.get(session["user_id"])
    세션에 user_id 있나?

    있으면 DB에서 User 객체 조회

    없으면 None

    여기서 "세션 조작 방어"가 자연스럽게 됨
    (없는 user_id면 DB 조회 결과 None)

        if not user:
    로그인 여부 판단 핵심
    user is None 이면

    로그인 안 했거나

    세션이 조작됐거나

    탈퇴/비활성화된 유저

            return redirect(url_for("auth.login"))
    인증 실패 처리
    로그인 페이지로 강제 이동

    view_func는 실행되지 않음

    즉,

    /home 요청
    → login_required
    → user 없음
    → /login으로 redirect
    → home()은 호출되지 않음
            return view_func(*args, **kwargs)
    인증 성공 시
    원래 요청했던 view 함수 실행

    GET / POST / URL 파라미터 그대로 전달

    /home 요청
    → login_required
    → user 있음
    → home() 실행
    → 정상 페이지 응답
        return decorated

    데코레이터의 핵심 구조
    @login_required
    def home():
        ...
    실제로는

    home = login_required(home)
    Flask는 home() 대신

    decorated()를 실행하게 됨

    전체 실행 흐름 한 줄 요약
    요청 →
    login_required →
    get_current_user() →
    로그인 안 됨? → /login redirect
    로그인 됨? → 원래 view 실행
    보안 관점에서 중요한 점
    세션 조작 걱정에 대한 답
    누가 session["user_id"]를 조작하면 로그인 되지 않나?

    거의 불가능 / 실질적으로 안전

    이유:

    Flask session은 SECRET_KEY로 서명됨

    user_id를 바꾸면 서명 깨짐

    서버에서 무조건 User.query.get()으로 검증

    없는 ID면 None → 접근 차단

    확장 포인트 (나중에)
    이 구조 덕분에 나중에 아래도 쉽게 가능

    def admin_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user = get_current_user()
            if not user or user.auth_level != "admin":
                abort(403)
            return f(*args, **kwargs)
        return decorated

    """
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        user = get_current_user()
        if not user:
            return redirect(url_for("auth.login"))
        return view_func(*args, **kwargs)
    return wrapped

def admin_required(view_func):
    """
    관리자 여부를 검사하는 데코레이터

    관리자 권한 검사 데코레이터
    (로그인 여부는 외부에서 보장)
    """
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        user = get_current_user()

        if user.auth_level != "admin":
            abort(403)

        return view_func(*args, **kwargs)
    return wrapped


def get_current_user():
    if "user_id" not in session:
        return None
    return User.query.get(session["user_id"])