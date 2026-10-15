"""Flask application factory and dependency injection setup."""
import os
from flask import Flask
from ..infrastructure.repositories import JsonCourseRepository, JsonEnrollmentRepository
from ..application.use_cases import (
    ListCoursesUseCase,
    GetCourseDetailUseCase,
    EnrollStudentUseCase,
    GetEnrollmentUseCase,
    GetInstructorProfileUseCase
)
from .routes import CourseWebController, create_course_blueprint


def create_app(test_config: dict | None = None) -> Flask:
    """Creates and configures the Flask application adhering to Hexagonal Architecture."""
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates"
    )

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-key-yoher-courses-2026"),
        COURSES_FILE=os.path.join(app.root_path, "../../data/courses.json"),
        ENROLLMENTS_FILE=os.path.join(app.root_path, "../../data/enrollments.json")
    )

    if test_config:
        app.config.update(test_config)

    # 1. Instantiate Infrastructure Adapters (Repositories)
    course_repo = JsonCourseRepository(app.config["COURSES_FILE"])
    enrollment_repo = JsonEnrollmentRepository(app.config["ENROLLMENTS_FILE"])

    # 2. Instantiate Application Use Cases (Injecting ports)
    list_courses_uc = ListCoursesUseCase(course_repo)
    get_course_detail_uc = GetCourseDetailUseCase(course_repo)
    enroll_student_uc = EnrollStudentUseCase(course_repo, enrollment_repo)
    get_enrollment_uc = GetEnrollmentUseCase(enrollment_repo, course_repo)
    get_instructor_uc = GetInstructorProfileUseCase()

    # 3. Instantiate Web Controller (Injecting use cases)
    controller = CourseWebController(
        list_courses_uc=list_courses_uc,
        get_course_detail_uc=get_course_detail_uc,
        enroll_student_uc=enroll_student_uc,
        get_enrollment_uc=get_enrollment_uc,
        get_instructor_uc=get_instructor_uc
    )

    # 4. Register Blueprint
    bp = create_course_blueprint(controller)
    app.register_blueprint(bp)

    @app.errorhandler(404)
    def not_found_error(error):
        return (
            """<!doctype html>
            <html lang="es">
            <head><meta charset="utf-8"><title>404 - Página no encontrada</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>
            <body class="bg-light text-center py-5">
                <div class="container py-5">
                    <h1 class="display-3 fw-bold text-primary">404</h1>
                    <p class="fs-4 text-secondary">El recurso o curso que buscas no fue encontrado.</p>
                    <a href="/" class="btn btn-primary px-4 py-2 mt-3">Volver al Inicio</a>
                </div>
            </body>
            </html>""",
            404
        )

    return app
