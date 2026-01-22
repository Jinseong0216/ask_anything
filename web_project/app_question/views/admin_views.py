from flask import Blueprint, render_template, redirect, url_for
from app_question.utils.auth import login_required, admin_required
from app_question.models import User, Question

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/")
@login_required
@admin_required
def dashboard():
    return render_template("admin/dashboard.html")


@bp.route("/users")
@login_required
@admin_required
def user_list():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=users)


@bp.route("/questions")
@login_required
@admin_required
def question_list():
    questions = Question.query.order_by(Question.created_at.desc()).all()
    return render_template("admin/questions.html", questions=questions)
