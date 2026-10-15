"""Web presentation layer: Controllers and Flask routes."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from ..application.dtos import EnrollmentRequestDTO
from ..application.use_cases import (
    ListCoursesUseCase,
    GetCourseDetailUseCase,
    EnrollStudentUseCase,
    GetEnrollmentUseCase,
    GetInstructorProfileUseCase
)
from ..domain.exceptions import CourseNotFoundError


class CourseWebController:
    """Object-Oriented Controller handling HTTP requests and orchestrating application use cases."""

    def __init__(
        self,
        list_courses_uc: ListCoursesUseCase,
        get_course_detail_uc: GetCourseDetailUseCase,
        enroll_student_uc: EnrollStudentUseCase,
        get_enrollment_uc: GetEnrollmentUseCase,
        get_instructor_uc: GetInstructorProfileUseCase
    ):
        self._list_courses_uc = list_courses_uc
        self._get_course_detail_uc = get_course_detail_uc
        self._enroll_student_uc = enroll_student_uc
        self._get_enrollment_uc = get_enrollment_uc
        self._get_instructor_uc = get_instructor_uc

    def index(self):
        """Landing page displaying hero, featured courses, instructor preview, and benefits."""
        courses = self._list_courses_uc.execute()
        instructor = self._get_instructor_uc.execute()
        return render_template("index.html", courses=courses, instructor=instructor)

    def courses_list(self):
        """Dedicated catalog of available courses."""
        courses = self._list_courses_uc.execute()
        instructor = self._get_instructor_uc.execute()
        return render_template("courses.html", courses=courses, instructor=instructor)

    def course_detail(self, slug: str):
        """Individual course view with full description, syllabus, requirements, and pricing."""
        try:
            course = self._get_course_detail_uc.execute_by_slug(slug)
            instructor = self._get_instructor_uc.execute()
            return render_template("course_detail.html", course=course, instructor=instructor)
        except CourseNotFoundError:
            abort(404)

    def enroll_view(self, slug: str):
        """Displays the custom enrollment form for a specific course."""
        try:
            course = self._get_course_detail_uc.execute_by_slug(slug)
            return render_template("enroll.html", course=course, form_data={}, errors={})
        except CourseNotFoundError:
            abort(404)

    def process_enrollment(self, slug: str):
        """Handles submission of the course enrollment form using OOP DTOs and validation."""
        try:
            course = self._get_course_detail_uc.execute_by_slug(slug)
        except CourseNotFoundError:
            abort(404)

        # Build DTO from request
        request_dto = EnrollmentRequestDTO(
            course_slug=slug,
            student_name=request.form.get("student_name", "").strip(),
            student_email=request.form.get("student_email", "").strip(),
            student_phone=request.form.get("student_phone", "").strip(),
            experience_level=request.form.get("experience_level", "Principiante"),
            comments=request.form.get("comments", "").strip()
        )

        response_dto = self._enroll_student_uc.execute(request_dto)

        if not response_dto.success:
            flash(response_dto.message, "danger")
            return render_template(
                "enroll.html",
                course=course,
                form_data=request.form,
                errors=response_dto.errors or {}
            )

        flash(response_dto.message, "success")
        return redirect(url_for("courses.enrollment_success", slug=slug, enrollment_id=response_dto.enrollment_id))

    def enrollment_success(self, slug: str, enrollment_id: str):
        """Confirmation page upon successful enrollment."""
        data = self._get_enrollment_uc.execute(enrollment_id)
        if not data:
            abort(404)
        return render_template("enroll_success.html", enrollment=data["enrollment"], course=data["course"])

    def about(self):
        """Dedicated page about the instructor Yoher Vazquez, education vision, and credentials."""
        instructor = self._get_instructor_uc.execute()
        courses = self._list_courses_uc.execute()
        return render_template("about.html", instructor=instructor, courses=courses)

    def api_courses(self):
        """REST API endpoint returning all courses in JSON format."""
        courses = self._list_courses_uc.execute()
        return jsonify([c.to_dict() for c in courses])


def create_course_blueprint(controller: CourseWebController) -> Blueprint:
    """Configures the Flask Blueprint with routes bound to the controller instance."""
    bp = Blueprint("courses", __name__)

    bp.add_url_rule("/", view_func=controller.index, methods=["GET"])
    bp.add_url_rule("/cursos", view_func=controller.courses_list, methods=["GET"])
    bp.add_url_rule("/cursos/<slug>", view_func=controller.course_detail, methods=["GET"])
    bp.add_url_rule("/cursos/<slug>/inscribirse", view_func=controller.enroll_view, methods=["GET"])
    bp.add_url_rule("/cursos/<slug>/inscribirse", view_func=controller.process_enrollment, methods=["POST"])
    bp.add_url_rule("/cursos/<slug>/exito/<enrollment_id>", view_func=controller.enrollment_success, methods=["GET"])
    bp.add_url_rule("/nosotros", view_func=controller.about, methods=["GET"])
    bp.add_url_rule("/api/cursos", view_func=controller.api_courses, methods=["GET"])

    return bp
