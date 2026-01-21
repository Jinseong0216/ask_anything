"""
이 파일은 Flask 웹 애플리케이션의 진입점이다.

역할:
- Flask 서버 실행
- 데이터베이스 설정
- 회원(User) 모델 정의
- 회원가입 / 로그인 기능 제공

설계 의도:
- 최대한 가볍게 구성
- SQLite 사용 (무료, 서버 부담 없음)
- 나중에 질문 기능, 관리자 기능 확장 가능
"""

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

# Flask 애플리케이션 객체 생성
app = Flask(__name__)

# --------------------------------------------------
# 기본 설정
# --------------------------------------------------

# 세션, 보안 관련 기능에 사용되는 키
# 개발 단계이므로 간단한 문자열 사용
app.config["SECRET_KEY"] = "dev-secret-key"

# SQLite 데이터베이스 사용
# app.db 파일이 프로젝트 폴더에 생성됨
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

# SQLAlchemy 내부 추적 기능 비활성화
# 성능 및 경고 제거 목적
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Flask 앱과 SQLAlchemy 연결
db = SQLAlchemy(app)

# --------------------------------------------------
# 데이터베이스 모델 정의
# --------------------------------------------------

class User(db.Model):
    """
    사용자 정보를 저장하는 테이블

    목적:
    - 회원가입 정보 저장
    - 로그인 시 사용자 인증에 사용

    컬럼 설명:
    - id: 사용자 고유 번호
    - username: 로그인 ID (중복 불가)
    - password_hash: 암호화된 비밀번호
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

# --------------------------------------------------
# 로그인 여부 확인
# --------------------------------------------------

def login_required(func):
    """
    로그인 여부를 확인하는 데코레이터

    목적:
    - 로그인하지 않은 사용자의 페이지 접근 차단
    - 로그인 페이지로 자동 이동
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return wrapper

# --------------------------------------------------
# 회원가입 페이지
# --------------------------------------------------


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    회원가입 처리

    GET:
    - 회원가입 입력 화면 표시

    POST:
    - 입력된 회원 정보를 DB에 저장
    - 비밀번호는 반드시 암호화하여 저장
    """

    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        # 이미 존재하는 아이디인지 확인
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "이미 존재하는 아이디입니다."

        # 비밀번호를 해시 처리하여 저장
        password_hash = generate_password_hash(password)

        # User 객체 생성
        new_user = User(
            username=username,
            password_hash=password_hash
        )

        # DB에 저장
        db.session.add(new_user)
        db.session.commit()

        # 회원가입 완료 후 로그인 페이지로 이동
        return redirect(url_for("login"))

    return render_template("register.html")

# --------------------------------------------------
# 로그인 페이지
# --------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    로그인 처리

    GET:
    - 로그인 화면 표시

    POST:
    - 입력된 아이디와 비밀번호 확인
    - DB에 저장된 정보와 비교
    - 로그인 성공 시 세션에 사용자 정보 저장
    """

    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        # 아이디로 사용자 검색
        user = User.query.filter_by(username=username).first()

        # 사용자가 존재하고 비밀번호가 일치하는 경우
        if user and check_password_hash(user.password_hash, password):
            # 로그인 상태를 유지하기 위해 세션에 사용자 정보 저장
            session["user_id"] = user.id
            session["username"] = user.username

            # 로그인 성공 후 메인 페이지로 이동
            return redirect(url_for("home"))

        # 로그인 실패 시 다시 로그인 페이지로 이동
        return "아이디 또는 비밀번호가 틀렸습니다."

    return render_template("login.html")

# --------------------------------------------------
# 메인 페이지 (로그인 필수)
# --------------------------------------------------

@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    """
    로그인한 사용자만 접근 가능한 메인 페이지

    GET:
    - 질문 입력 화면 표시

    POST:
    - 질문 제출 처리
    """

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        problem = request.form.get("problem", "").strip()

        if not name:
            name = "익명"

        # 현재는 DB 저장 대신 출력만
        print("질문 도착")
        print("이름:", name)
        print("문제 번호:", problem)
        print("작성자:", session.get("username"))
        print("-" * 30)

        return render_template("index.html", success=True)

    return render_template("index.html", success=False)

# --------------------------------------------------
# 로그아웃
# --------------------------------------------------

@app.route("/logout")
def logout():
    """
    로그아웃 처리

    목적:
    - 세션 정보 삭제
    - 로그인 상태 해제
    """

    session.clear()
    return redirect(url_for("login"))

# --------------------------------------------------
# 서버 실행
# --------------------------------------------------

if __name__ == "__main__":
    # 앱 실행 시 최초 1회 DB 테이블 생성
    with app.app_context():
        db.create_all()

    # 배포 환경(PORT 환경변수)과 로컬 환경 모두 대응
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
