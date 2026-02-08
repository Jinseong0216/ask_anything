'''
앱 실행: flask --app  app_question:create_app run

db 생성: flask --app app_question:create_app db init
    데이터베이스를 초기화하는 flask db init 명령은 최초 한 번만 수행하면 된다.

flask --app app_question:create_app db migrate	
    모델을 새로 생성하거나 변경할 때 사용 (실행하면 작업파일이 생성된다.)

flask --app app_question:create_app db upgrade	
    모델의 변경 내용을 실제 데이터베이스에 적용할 때 사용 (위에서 생성된 작업파일을 실행하여 데이터베이스를 변경한다.)

flask shell 실행: flask --app app_question:create_app shell

로컬 호스팅: flask --app  app_question:create_app run --host=0.0.0.0 --port=5000
'''

from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


# 보안관련
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from flask_jwt_extended import JWTManager, verify_jwt_in_request
from werkzeug.exceptions import Unauthorized
from datetime import timedelta

from .context import inject_globals
from . import config

# create_app 내부에서 생성하지 않고,
# 전역에서 선언 후 init_app 패턴 사용
# (Blueprint, model import 문제 방지)
jwt = JWTManager()
bcrypt = Bcrypt()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

CSRF_EXEMPT_PATHS = {
    "/api/auth/login",
    "/api/auth/register",
    "/api/auth/logout",
}


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # 차후 수정 (키)
    app.config["SECRET_KEY"] = config.SECRET_KEY
    app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY

    # -------------------------
    # JWT (Cookie 기반 인증)
    # -------------------------
    app.config.update(
        JWT_TOKEN_LOCATION=["cookies"],

        # 만료시간
        JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1),
        JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30),

        # Access Token
        JWT_ACCESS_COOKIE_NAME = "access_token",
        JWT_ACCESS_COOKIE_PATH = "/",
        JWT_REFRESH_COOKIE_NAME = "refresh_token",
        JWT_REFRESH_COOKIE_PATH = "/",

        # Cookie security
        JWT_COOKIE_SECURE = True,      # HTTPS 환경에서는 True
        JWT_COOKIE_HTTPONLY = True,
        JWT_COOKIE_SAMESITE = "Lax",    # Cross-site 필요 시 None + Secure

        # CSRF protection
        JWT_CSRF_IN_COOKIES = False,
        # JWT_CSRF_HEADER_NAME = "X-CSRF-TOKEN",
        JWT_COOKIE_CSRF_PROTECT = False     # CSRF 보호 끔 (개발용)
    )


    # config.py 파일에 작성한 항목을 읽기 위해 app.config.from_object(config) 코드를 추가
    app.config.from_object(config)


    # 전역 변수로 db, migrate 객체를 만든 다음 create_app 함수 안에서 init_app 메서드를 이용해 app에 등록
    # db 객체를 create_app 함수 안에서 생성하면 블루프린트와 같은 다른 모듈에서 사용할수 없기 때문에 db, 
    #   migrate와 같은 객체를 create_app 함수 밖에 생성하고, 
    #   해당 객체를 앱에 등록할 때는 create_app 함수에서 init_app 함수를 통해 진행
    db.init_app(app)
    migrate.init_app(app, db)

    jwt.init_app(app)
    bcrypt.init_app(app)
    limiter.init_app(app)

    # -------------------------
    # CORS (Vue + Cookie)
    # -------------------------
    CORS(
        app,
        supports_credentials=True,
        resources={
            r"/api/*": {"origins": "https://localhost:8080"}
        },
    )

    # 전역변수 등록
    app.context_processor(inject_globals)

    # 모델을 플라스크의 migrate 기능이 인식
    from . import models

    # 블루프린트
    from .views import test_views, api_auth_views
    app.register_blueprint(api_auth_views.bp)
    app.register_blueprint(test_views.bp)

    from flask import request, abort

    # CSRF Middleware (Double Submit)
    @app.before_request
    def csrf_protect():
        
        # CSRF 예외
        if request.path in CSRF_EXEMPT_PATHS:
            return
        
        # GET / OPTIONS / HEAD 제외
        if request.method not in ("POST", "PUT", "PATCH", "DELETE"):
            return
        
        # JWT 먼저 검증
        try:
            verify_jwt_in_request()

        except Unauthorized:
            return jsonify({"msg": "Unauthorized"}), 401

        # CSRF 토큰 비교
        csrf_cookie = request.cookies.get("csrf_token")
        csrf_header = request.headers.get("X-CSRF-TOKEN")

        print('csrf_cookie', csrf_cookie)
        print('csrf_header', csrf_header)

        if not csrf_cookie or not csrf_header:
            print('No CSRF TOKEN \n\n\n')
            return jsonify({"msg": "CSRF token missing"}), 403

        if csrf_cookie != csrf_header:
            print('No CSRF TOKEN HEADER \n\n\n')
            return jsonify({"msg": "Invalid CSRF token"}), 403
        print('Valid CSRF TOKEN \n\n\n')

    return app

# flask --app app_question run  --port=5000  --cert=cert/localhost.pem  --key=cert/localhost-key.pem
