from flask import Blueprint, request, jsonify, make_response, abort

from app_question import db, bcrypt
from app_question.models import User

from flask_jwt_extended import (
    get_jwt,
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
    get_csrf_token,
    unset_jwt_cookies,
    verify_jwt_in_request,
    jwt_required,
    get_jwt_identity,
    decode_token,
)
from flask_jwt_extended.exceptions import NoAuthorizationError

from flask_limiter import Limiter
import secrets
from app_question.models import RefreshToken
from app_question.utils.auth import generate_tokens, store_refresh_token

from app_question.utils.auth import role_required

bp = Blueprint('api_auth', __name__, url_prefix='/api/auth')


# =========================
# 회원가입
# =========================
@bp.post("/register")
def register():
    print("register 요청")
    data = request.get_json() or {}

    login_id = data.get("login_id").strip()
    password = data.get("password")
    user_name = data.get("user_name").strip()
    email = data.get("email").strip()

    # 기본 입력값 검증
    if not all([login_id, password, user_name, email]):
        return jsonify(msg="invalid input"), 400

    # 중복 체크
    if User.query.filter_by(login_id=login_id).first():
        return jsonify(msg="login_id exists"), 409

    if User.query.filter_by(email=email).first():
        return jsonify(msg="email exists"), 409

    # 비밀번호 해시
    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(
        login_id=login_id,
        password_hash=password_hash,
        user_name=user_name,
        email=email,
    )

    try:
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify(message="duplicated_user"), 409
    
    return jsonify(msg="registered"), 201


# =========================
# 로그인
# =========================
@bp.post("/login")
def login():
    print("====== login api 요청 =====")
    print(request.headers)
    data = request.get_json()
    login_id = data.get("login_id")
    password = data.get("password")

    if not login_id or not password:
        return jsonify(msg="invalid input"), 400

    user = User.query.filter_by(login_id=login_id).first()

    # 계정 존재 여부
    if not user:
        return jsonify(msg="invalid user"), 403    

    # 비활성 계정 차단
    if not user.is_active:
        return jsonify(msg="inactive account"), 403

    # 비밀번호 검증
    if not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify(msg="invalid credentials"), 403
    

    # JWT에는 user_id만 담는다
    access_token, refresh_token = generate_tokens(user)
    response = make_response(jsonify(msg="login success"))
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    store_refresh_token(refresh_token, user.user_id)

    print('login api 응답 headers 출력\n', response.headers)

    csrf_token = secrets.token_hex(32)
    response.set_cookie(
        "csrf_token",
        csrf_token,
        httponly=False,
        secure=True,
        samesite="Lax",
        path="/"
    )
    return response


# =========================
# 로그인 상태 확인
# =========================
@bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    print('me 체크', user)

    # 토큰은 유효하지만 사용자 없음 → 강제 로그아웃
    if not user:
        return jsonify(msg="user not found"), 403
    # 토큰은 유효하지만 비활성화된 사용자 → 강제 로그아웃
    if not user.is_active:
        return jsonify(msg="user deactivated"), 403
    

    return jsonify(
        user_id=user.user_id,
        login_id=user.login_id,
        user_name=user.user_name,
        email=user.email,
        role=user.role,
        auth_level=user.auth_level,
    )

# =========================
# 로그아웃
# =========================
@bp.post("/logout")
def logout():
    user_id = None

    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
    except NoAuthorizationError:
        pass

    if user_id:
        RefreshToken.query.filter_by(
            user_id=user_id,
            revoked=False
        ).update({"revoked": True})
        db.session.commit()

    response = jsonify({"msg": "logout"})
    unset_jwt_cookies(response)
    return response


# =========================
#refresh_token 사용
# =========================
@bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    jwt_data = get_jwt()
    user_id = get_jwt_identity()
    old_jti = jwt_data["jti"]

    user = User.query.get(user_id)

    token_row = RefreshToken.query.filter_by(
        jti=old_jti,
        revoked=False
    ).first()

    # 재사용 → 공격 가능성
    if not token_row:
        abort(401)

    token_row.revoked = True
    db.session.commit()

    # 새 토큰 발급
    access_token, refresh_token = generate_tokens(user)
    store_refresh_token(refresh, user.user_id)

    response = jsonify({"msg": "refreshed"})
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    # user = User.query.get(user_id)
    # if not user or not user.is_active:
    #     return jsonify(msg="invalid user"), 403

    # access_token = create_access_token(identity=str(user.user_id))
    # res = jsonify(msg="refreshed")
    # set_access_cookies(res, access_token)
    return response


# 권한확인 api
@bp.get("/check_admin")
@jwt_required()
@role_required("admin")
def admin_only():
    return jsonify({"msg": "admin access granted"})