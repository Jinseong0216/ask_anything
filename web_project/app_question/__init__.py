'''
앱 실행: flask --app  app_question:create_app run

db 생성: flask --app app_question:create_app db init
    데이터베이스를 초기화하는 flask db init 명령은 최초 한 번만 수행하면 된다.

flask --app app_question:create_app db migrate	
    모델을 새로 생성하거나 변경할 때 사용 (실행하면 작업파일이 생성된다.)

flask --app app_question:create_app db upgrade	
    모델의 변경 내용을 실제 데이터베이스에 적용할 때 사용 (위에서 생성된 작업파일을 실행하여 데이터베이스를 변경한다.)

flask shell 실행: flask --app app_question:create_app shell
'''

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from . import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # 차후 수정 (키)
    app.config["SECRET_KEY"] = "dev-secret-key-change-this"

    # config.py 파일에 작성한 항목을 읽기 위해 app.config.from_object(config) 코드를 추가
    app.config.from_object(config)

    # 전역 변수로 db, migrate 객체를 만든 다음 create_app 함수 안에서 init_app 메서드를 이용해 app에 등록
    # db 객체를 create_app 함수 안에서 생성하면 블루프린트와 같은 다른 모듈에서 사용할수 없기 때문에 db, 
    #   migrate와 같은 객체를 create_app 함수 밖에 생성하고, 
    #   해당 객체를 앱에 등록할 때는 create_app 함수에서 init_app 함수를 통해 진행
    db.init_app(app)
    migrate.init_app(app, db)
    # 모델을 플라스크의 migrate 기능이 인식
    from . import models

    # 앱 컨텍스트 안에서 테이블 생성
    with app.app_context():
        db.create_all()

    # 블루프린트
    from .views import main_views, auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)
    return app