from flask import abort
from functools import wraps

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    verify_jwt_in_request,
    get_jwt
)
from flask_jwt_extended import decode_token
from datetime import datetime
from app_question import db
from app_question.models import User, RefreshToken

# 토큰 생성 함수

def generate_tokens(user):
    """
    Access:
    - 짧은 수명
    - role 포함 (권한 체크용)

    Refresh:
    - 긴 수명
    - 재발급 전용
    """
    access_token = create_access_token(
        identity=str(user.user_id),
        additional_claims={
            "auth_level": user.auth_level,
            "role": user.role
        }
    )

    refresh_token = create_refresh_token(
        identity=str(user.user_id),
        additional_claims={
            "auth_level": user.auth_level,
            "role": user.role
        }
    )

    return access_token, refresh_token

# 서버에 refresh 토큰 저장
def store_refresh_token(token, user_id):
    """
    Refresh Token을 DB에 저장
    → 회전/폐기 추적 목적
    """
    decoded = decode_token(token)

    db.session.add(
        RefreshToken(
            user_id=user_id,
            jti=decoded["jti"],
            expires_at=datetime.fromtimestamp(decoded["exp"]),
            revoked=False
        )
    )
    db.session.commit()

# 권한 관련
Auth_LEVEL = {
    "general": 1,
    "admin": 2,
}
def auth_required(min_auth):
    def wrapper(view_func):
        @wraps(view_func)
        def decorated(*args, **kwargs):
            verify_jwt_in_request()
            auth = get_jwt().get("auth_level")
            print('권한레벨 확인', auth)
            if Auth_LEVEL.get(auth, 0) < Auth_LEVEL[min_auth]:
                abort(403)

            return view_func(*args, **kwargs)
        return decorated
    return wrapper