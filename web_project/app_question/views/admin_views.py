from flask import Blueprint, render_template, redirect, url_for, session, abort
from app_question.utils.auth import login_required, admin_required
from app_question.models import User, Question
from app_question import db

from sqlalchemy import func

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
    if session.get("auth_level") != 'admin': abort(403)

    question_count_by_users = (
        db.session.query(
            User.user_id,
            User.user_name,
            func.count(Question.question_id).label("question_count")
        )
        .join(Question)
        .filter(User.role == 'student')
        .group_by(User.user_id)
        .all()
    )
    
    questions = (
        Question.query
        .join(User)
        .filter(User.role == 'student')
        .order_by(Question.created_at.desc())
        .all()
    )

    return render_template(
        "admin/questions.html",
        summary = question_count_by_users,
        questions = questions
    )