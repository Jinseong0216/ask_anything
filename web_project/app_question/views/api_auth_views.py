from flask import Blueprint, request, jsonify

from app_question import db, bcrypt
from app_question.models import User

from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    jwt_required,
    get_jwt_identity,
)
from flask_limiter import Limiter


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
    data = request.get_json()

    login_id = data.get("login_id")
    password = data.get("password")

    if not login_id or not password:
        return jsonify(msg="invalid input"), 400

    user = User.query.filter_by(login_id=login_id).first()

    # 계정 존재 여부
    if not user:
        return jsonify(msg="invalid credentials"), 401

    # 비활성 계정 차단
    if not user.is_active:
        return jsonify(msg="inactive account"), 403

    # 비밀번호 검증
    if not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify(msg="invalid credentials"), 401

    # JWT에는 user_id만 담는다
    access_token = create_access_token(identity=user.user_id)

    response = jsonify(msg="login success")
    set_access_cookies(response, access_token)

    return response


# =========================
# 로그인 상태 확인
# =========================
@bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user or not user.is_active:
        return jsonify(msg="invalid user"), 401

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
    response = jsonify(msg="logout")
    unset_jwt_cookies(response)
    return response