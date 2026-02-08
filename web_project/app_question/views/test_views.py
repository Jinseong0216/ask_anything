from flask import Blueprint, render_template, request, redirect, url_for, session
from app_question.models import Question
from app_question import db

bp = Blueprint('test', __name__, url_prefix='/test')

# 테스트 viewfucntion

@bp.route('/', methods=["GET", "POST"])
def test_main():
    return render_template("test_templates/main_page.html")


@bp.route('/dashboard', methods=["GET", "POST"])
def test_dashboard():
    return render_template("test_templates/dashboard.html")