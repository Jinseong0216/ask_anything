"""
인증 관련 뷰 모음

역할:
- 회원가입 처리
- 로그인 처리
- 로그아웃 처리

이 파일은 사용자 인증 흐름만 담당하며,
비즈니스 로직이나 DB 구조 정의는 포함하지 않는다.
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app_question import db
from app_question.models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_id = request.form.get("login_id", "").strip()
        password = request.form.get("password", "").strip()

        user = User.query.filter_by(login_id=login_id, is_active=True).first()

        # 로그인 성공
        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.user_id
            session["login_id"] = user.login_id
            session["user_name"] = user.user_name
            session["role"] = user.role
            session["auth_level"] = user.auth_level
            return redirect(url_for("main.home"))
        
        # 로그인 실패
        else:
            flash("아이디 또는 비밀번호가 올바르지 않습니다.")
            return redirect(url_for("auth.login"))

    return render_template("login/login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login_id = request.form.get("login_id", "").strip()
        user_name = request.form.get("user_name", "").strip()
        password = request.form.get("password", "").strip()

        if not login_id or not user_name or not password:
            return "모든 항목을 입력해야 합니다."

        if User.query.filter_by(login_id=login_id).first():
            return "이미 사용 중인 아이디입니다."

        user = User(
            login_id=login_id,
            user_name=user_name,
            password_hash=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("register/register.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))