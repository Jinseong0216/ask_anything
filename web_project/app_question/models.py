"""
데이터베이스 모델 정의 파일

이 파일은 애플리케이션에서 사용하는 모든 DB 테이블 구조를 정의한다.
Flask 애플리케이션 객체는 생성하지 않으며,
이미 생성된 SQLAlchemy 객체(db)를 import하여 모델만 선언한다.

이 구조를 사용하는 이유:
- DB 구조를 한 곳에서 관리하기 위함
- 뷰, 비즈니스 로직과 DB 설계를 분리하기 위함
- 나중에 마이그레이션 도구(flask-migrate) 사용을 고려함
"""

from app_question import db
from datetime import datetime

class User(db.Model):
    """
    사용자(회원) 정보를 저장하는 테이블

    이 테이블은 로그인 인증 및 사용자 식별의 기준이 된다.
    질문, 로그, 관리자 기능 등 모든 사용자 기반 기능은
    이 테이블의 user_id를 기준으로 연결되도록 설계한다.
    """

    # 실제 데이터베이스에 생성될 테이블 이름
    # SQL 예약어(user)와의 충돌을 피하기 위해 users로 명시
    __tablename__ = "users"

    # 내부적으로 사용하는 고유 식별자
    # 다른 테이블과의 관계(FK)에서 기준이 되는 값
    user_id = db.Column(db.Integer, primary_key=True)

    # 로그인 시 사용하는 계정 ID
    # 영문/숫자 기준으로 사용, 시스템 내부 식별 용도
    # 외부 노출이나 표시 용도로는 사용하지 않음
    login_id = db.Column(db.String(50), unique=True, nullable=False)

    # 비밀번호 해시 값
    # 원본 비밀번호는 절대 저장하지 않음
    # werkzeug.security.generate_password_hash() 결과 저장
    password_hash = db.Column(db.String(255), nullable=False)

    # 사용자 이름 (표시용)
    # 한글 입력을 허용하기 위해 길이를 넉넉하게 설정
    # 학부모, 관리자 화면 등에서 사용자 식별용으로 사용
    user_name = db.Column(db.String(100), nullable=False)

    # 이메일
    email = db.Column(db.String(120), unique=True, nullable=False)


    # 계정 생성 시각
    # 회원가입 시점 기록용
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    # 역할 (student / teacher / ...)
    role = db.Column(db.String(20), default="student", nullable=False)

    # 권한 레벨 (general / admin / ...)
    auth_level = db.Column(db.String(20), default="general", nullable=False)    

    # 계정 활성 상태
    # 탈퇴 처리 시 실제 삭제 대신 비활성화 용도로 사용
    # True  : 정상 사용자
    # False : 비활성 / 탈퇴 처리
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        """
        디버깅 및 로그 출력 시 사용

        객체를 출력했을 때 어떤 사용자인지 바로 알 수 있도록
        login_id와 user_id를 함께 표시한다.
        """
        return f"<User user_id={self.user_id}, login_id={self.login_id}>"

class Question(db.Model):
    __tablename__ = "questions"

    question_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    grade = db.Column(db.String(10), nullable=False)
    book = db.Column(db.String(50), nullable=False)
    question_num = db.Column(db.String(20), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="questions")




class RefreshToken(db.Model):
    __tablename__ = "refresh_tokens"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable=False
    )

    # JWT 고유 식별자
    jti = db.Column(db.String(36), unique=True, nullable=False)

    expires_at = db.Column(db.DateTime, nullable=False)

    revoked = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)