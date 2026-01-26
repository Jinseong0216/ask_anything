'''
SQLALCHEMY_DATABASE_URI는 데이터베이스 접속 주소이고 
SQLALCHEMY_TRACK_MODIFICATIONS는 SQLAlchemy의 이벤트를 처리하는 옵션이다. 
이 옵션은 app_question에 필요하지 않으므로 False로 비활성화하자. 

SQLALCHEMY_DATABASE_URI 설정에 의해 SQLite 데이터베이스가 사용되고 
데이터베이스 파일은 프로젝트 홈 디렉터리 바로 밑에 app_question.db 파일로 저장된다.
'''

import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'app_question.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "dev-secret-key-change-this"
JWT_SECRET_KEY = "dev-jwt-secret-key-change-this"
