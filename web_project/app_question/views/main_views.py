from flask import Blueprint, render_template, request, redirect, url_for, session
from app_question.models import Question
from app_question import db
from app_question.utils.auth import login_required

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'

@bp.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        problem = request.form.get("problem")

        print("질문 도착")
        print("문제 번호:", problem)

    return render_template("index.html")


@bp.route("/question", methods=["GET", "POST"])
@login_required
def question():
    if request.method == "POST":
        grade = request.form.get("grade")
        book = request.form.get("book")
        question_num = request.form.get("question_num")

        # 로그인 사용자
        user_id = session.get("user_id")

        # 질문 저장
        question = Question(
            user_id = user_id,
            grade = grade,
            book = book,
            question_num = question_num
        )

        db.session.add(question)
        db.session.commit()

        return redirect(url_for("main.question"))
    
    return render_template("index.html")


@bp.route("/mypage", methods=["GET", "POST"])
@login_required
def mypage():
    if request.method == "POST":
        # 마이페이지 내용 수정관련
        pass
        return 
    
    return render_template("mypage.html")
#    return render_template("mypage.html")