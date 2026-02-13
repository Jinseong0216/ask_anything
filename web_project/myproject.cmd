@echo off

REM 이 cmd 파일 위치로 이동
cd /d %~dp0

REM 가상환경 활성화
call venv\Scripts\activate

REM Flask 설정
set FLASK_APP=app_question
set FLASK_DEBUG=1

REM Flask 실행
flask run

pause
