"""Pruebas unitarias para los componentes y vistas de la GUI en Flet con POO."""
import os
import unittest
from src.infrastructure.repositories import JsonCourseRepository, JsonEnrollmentRepository
from src.application.use_cases import (
    ListCoursesUseCase,
    GetCourseDetailUseCase,
    EnrollStudentUseCase,
    GetInstructorProfileUseCase
)
from src.gui.views import (
    CourseCardComponent,
    HomeView,
    CoursesView,
    CourseDetailView,
    EnrollmentView,
    EnrollmentListView,
    AboutView
)


class TestFletGUIOOPStructure(unittest.TestCase):
    """Verifica la arquitectura y diseño de clases orientado a objetos de la GUI Flet."""

    def setUp(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.courses_file = os.path.join(base_dir, "data", "courses.json")
        self.enrollments_file = os.path.join(base_dir, "data", "enrollments.json")

        self.course_repo = JsonCourseRepository(self.courses_file)
        self.enrollment_repo = JsonEnrollmentRepository(self.enrollments_file)

        self.list_courses_uc = ListCoursesUseCase(self.course_repo)
        self.get_course_detail_uc = GetCourseDetailUseCase(self.course_repo)
        self.enroll_student_uc = EnrollStudentUseCase(self.course_repo, self.enrollment_repo)
        self.get_instructor_uc = GetInstructorProfileUseCase()

    def test_course_card_component_build(self):
        courses = self.list_courses_uc.execute()
        self.assertGreaterEqual(len(courses), 3)

        card_comp = CourseCardComponent(courses[0], lambda r, p: None)
        control = card_comp.build()
        self.assertIsNotNone(control)

    def test_views_initialization_and_build(self):
        # Verificar herencia de BaseView e inyección de dependencias
        home_view = HomeView(None, lambda r, p: None, self.list_courses_uc, self.get_instructor_uc)
        self.assertIsNotNone(home_view.build())

        courses_view = CoursesView(None, lambda r, p: None, self.list_courses_uc)
        self.assertIsNotNone(courses_view.build())

        detail_view = CourseDetailView(None, lambda r, p: None, self.get_course_detail_uc, "inteligencia-artificial-y-llms")
        self.assertIsNotNone(detail_view.build())

        enroll_view = EnrollmentView(None, lambda r, p: None, self.get_course_detail_uc, self.enroll_student_uc, "inteligencia-artificial-y-llms")
        self.assertIsNotNone(enroll_view.build())

        list_view = EnrollmentListView(None, lambda r, p: None, self.enrollment_repo)
        self.assertIsNotNone(list_view.build())

        about_view = AboutView(None, lambda r, p: None, self.get_instructor_uc)
        self.assertIsNotNone(about_view.build())


if __name__ == "__main__":
    unittest.main()
