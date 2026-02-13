from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app_question import db
from app_question.models import User, Lecture, LectureTeacher, LectureStudent
from app_question.utils.utils import generate_invite_code


bp = Blueprint("lecture", __name__, url_prefix="/api/lectures")


@bp.route("/register", methods=["POST"])
@jwt_required()
def create_lecture():
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    # 권한 체크
    if user.role != "teacher":
        return jsonify({"msg": "강사만 수업을 생성할 수 있습니다."}), 403

    data = request.get_json()

    title = data.get("title")

    if not title:
        return jsonify({"msg": "강의 제목은 필수입니다."}), 400

    # 초대코드 생성 (중복 방지 루프)
    while True:
        invite_code = generate_invite_code()
        if not Lecture.query.filter_by(invite_code=invite_code).first():
            break

    # 강의 생성
    lecture = Lecture(
        title=title,
        invite_code=invite_code,
        is_active=True
    )

    db.session.add(lecture)
    db.session.flush()  # lecture_id 확보

    # 생성한 강사를 공동강사 테이블에 등록 (OWNER 개념)
    lecture_teacher = LectureTeacher(
        lecture_id=lecture.lecture_id,
        teacher_id=user.user_id,
        role="owner"
    )

    db.session.add(lecture_teacher)
    db.session.commit()

    return jsonify({
        "msg": "강의 생성 완료",
        "lecture_title": lecture.title,
        "lecture_id": lecture.lecture_id,
        "invite_code": invite_code
    }), 201


@bp.route("/my", methods=["GET"])
@jwt_required()
def get_my_lectures():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)

    # 역할에 따라 강의 목록 선택
    lectures = (
        user.teaching_lectures
        if user.role == "teacher"
        else user.enrolled_lectures
    )

    result = []

    for lecture in lectures:
        if user.role == "teacher":
            result.append({
                "lecture_id": lecture.lecture_id,
                "title": lecture.title,
                "invite_code": lecture.invite_code,
                "created_at": lecture.created_at.isoformat(),
            })
        else:  # student
            result.append({
                "lecture_id": lecture.lecture_id,
                "title": lecture.title,
            })

    return jsonify(result)


@bp.post("/enroll")
@jwt_required()
def enroll_lecture():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    # 권한 체크
    if user.role != "student":
        return jsonify({"msg": "학생만 강의조회가 가능합다."}), 403

    data = request.get_json() or {}

    invite_code = data.get("invite_code")
    if not invite_code:
        return jsonify({"msg": "invite_code required"}), 400

    # 강의 찾기
    lecture = Lecture.query.filter_by(
        invite_code=invite_code,
        is_active=True
    ).first()

    if not lecture:
        return jsonify({"msg": "invalid invite code"}), 404

    # 이미 등록했는지 확인
    exists = LectureStudent.query.filter_by(
        lecture_id=lecture.lecture_id,
        student_id=user_id
    ).first()

    if exists:
        return jsonify({"msg": "already enrolled"}), 409

    # 등록
    enrollment = LectureStudent(
        lecture_id=lecture.lecture_id,
        student_id=user_id
    )

    db.session.add(enrollment)
    db.session.commit()

    return jsonify({"msg": "enrolled successfully"})