"""Comprehensive unit and integration tests for the Hexagonal Flask application."""
import json
import os
import tempfile
import unittest
from src.domain.entities import Course, Enrollment, Instructor, SyllabusModule
from src.domain.exceptions import CourseNotFoundError, InvalidEnrollmentError
from src.application.dtos import EnrollmentRequestDTO
from src.application.use_cases import (
    ListCoursesUseCase,
    GetCourseDetailUseCase,
    EnrollStudentUseCase
)
from src.infrastructure.repositories import JsonCourseRepository, JsonEnrollmentRepository
from src.web.app import create_app


class TestDomainEntities(unittest.TestCase):
    def test_course_entity(self):
        course = Course(
            id="c1",
            slug="curso-ia",
            title="Curso de IA",
            subtitle="Subtítulo",
            category="IA",
            level="Intermedio",
            duration="4 semanas",
            price=99.99,
            currency="USD",
            badge="Nuevo",
            cover_image="http://img.jpg",
            instructor_name="Yoher Vazquez",
            short_description="Desc corta",
            full_description="Desc larga",
            requirements=["Python"],
            syllabus=[SyllabusModule("Módulo 1", ["Tema 1", "Tema 2"])],
            tags=["AI", "Python"]
        )
        self.assertEqual(course.formatted_price, "$99.99 USD")
        self.assertFalse(course.is_free)
        self.assertEqual(len(course.syllabus), 1)

        # Serialization roundtrip
        data = course.to_dict()
        reconstituted = Course.from_dict(data)
        self.assertEqual(reconstituted.id, course.id)
        self.assertEqual(reconstituted.title, course.title)

    def test_enrollment_validation_success(self):
        enrollment = Enrollment(
            course_id="c1",
            student_name="Carlos Mendoza",
            student_email="carlos@example.com",
            student_phone="+584121234567",
            experience_level="Intermedio"
        )
        # Should not raise
        enrollment.validate()
        self.assertTrue(enrollment.id.startswith("ENR-"))

    def test_enrollment_validation_failure(self):
        enrollment = Enrollment(
            course_id="c1",
            student_name="Al",  # Too short
            student_email="invalid-email",
            student_phone="123",
            experience_level="Principiante"
        )
        with self.assertRaises(InvalidEnrollmentError) as ctx:
            enrollment.validate()
        self.assertIn("student_name", ctx.exception.errors)
        self.assertIn("student_email", ctx.exception.errors)


class TestRepositoriesAndUseCases(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.courses_file = os.path.join(self.temp_dir.name, "courses.json")
        self.enrollments_file = os.path.join(self.temp_dir.name, "enrollments.json")

        sample_courses = [
            {
                "id": "c1",
                "slug": "curso-test-ia",
                "title": "Curso Test IA",
                "subtitle": "Sub",
                "category": "IA",
                "level": "Intermedio",
                "duration": "4 semanas",
                "price": 100.0,
                "currency": "USD",
                "badge": "Top",
                "cover_image": "http://img.jpg",
                "instructor_name": "Yoher Vazquez",
                "short_description": "Corta",
                "full_description": "Larga",
                "requirements": ["Python"],
                "syllabus": [{"module": "M1", "topics": ["T1"]}],
                "tags": ["IA"]
            }
        ]
        with open(self.courses_file, "w", encoding="utf-8") as f:
            json.dump(sample_courses, f)

        self.course_repo = JsonCourseRepository(self.courses_file)
        self.enrollment_repo = JsonEnrollmentRepository(self.enrollments_file)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_list_courses_use_case(self):
        uc = ListCoursesUseCase(self.course_repo)
        courses = uc.execute()
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0].slug, "curso-test-ia")

    def test_get_course_detail_use_case(self):
        uc = GetCourseDetailUseCase(self.course_repo)
        course = uc.execute_by_slug("curso-test-ia")
        self.assertEqual(course.title, "Curso Test IA")

        with self.assertRaises(CourseNotFoundError):
            uc.execute_by_slug("inexistente")

    def test_enroll_student_use_case_success(self):
        uc = EnrollStudentUseCase(self.course_repo, self.enrollment_repo)
        dto = EnrollmentRequestDTO(
            course_slug="curso-test-ia",
            student_name="Ana Rodríguez",
            student_email="ana@example.com",
            student_phone="+123456789",
            experience_level="Avanzado",
            comments="Interesada en LLMs"
        )
        response = uc.execute(dto)
        self.assertTrue(response.success)
        self.assertIsNotNone(response.enrollment_id)

        # Check repository persistence
        saved = self.enrollment_repo.get_by_id(response.enrollment_id)
        self.assertIsNotNone(saved)
        self.assertEqual(saved.student_name, "Ana Rodríguez")


class TestFlaskWebRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            "TESTING": True
        })
        self.client = self.app.test_client()

    def test_landing_page(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Yoher Vazquez", res.text)
        self.assertIn("Inteligencia Artificial", res.text)
        self.assertIn("Cloudflare", res.text)
        self.assertIn("Cloud Computing", res.text)

    def test_courses_catalog_page(self):
        res = self.client.get("/cursos")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Catálogo de Cursos", res.text)

    def test_course_detail_page(self):
        res = self.client.get("/cursos/inteligencia-artificial-y-llms")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Plan de Estudios", res.text)
        self.assertIn("Requisitos Previos", res.text)

    def test_course_detail_404(self):
        res = self.client.get("/cursos/no-existe")
        self.assertEqual(res.status_code, 404)

    def test_about_page(self):
        res = self.client.get("/nosotros")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Yoher Vazquez", res.text)
        self.assertIn("Ingeniero en Informática", res.text)
        self.assertIn("Docente Universitario", res.text)

    def test_enroll_form_get(self):
        res = self.client.get("/cursos/inteligencia-artificial-y-llms/inscribirse")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Formulario de Inscripción", res.text)

    def test_enroll_form_post_invalid(self):
        res = self.client.post("/cursos/inteligencia-artificial-y-llms/inscribirse", data={
            "student_name": "J",  # Too short
            "student_email": "bademail",
            "student_phone": ""
        })
        self.assertEqual(res.status_code, 200)
        self.assertIn("Por favor ingresa", res.text)

    def test_enroll_form_post_success(self):
        res = self.client.post("/cursos/inteligencia-artificial-y-llms/inscribirse", data={
            "student_name": "Estudiante de Prueba",
            "student_email": "estudiante@prueba.com",
            "student_phone": "+584241234567",
            "experience_level": "Intermedio",
            "comments": "Excelente temario"
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("¡Inscripción registrada exitosamente!", res.text)
        self.assertIn("Código de Inscripción", res.text)

    def test_api_courses(self):
        res = self.client.get("/api/cursos")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 3)


if __name__ == "__main__":
    unittest.main()
