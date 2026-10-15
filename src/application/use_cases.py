"""Application use cases orchestrating domain entities and ports."""
from typing import List, Optional
from ..domain.entities import Course, Enrollment, Instructor
from ..domain.ports import CourseRepository, EnrollmentRepository
from ..domain.exceptions import CourseNotFoundError, InvalidEnrollmentError
from .dtos import EnrollmentRequestDTO, EnrollmentResponseDTO


class ListCoursesUseCase:
    """Use case to retrieve the complete catalog of courses."""

    def __init__(self, course_repo: CourseRepository):
        self._course_repo = course_repo

    def execute(self) -> List[Course]:
        return self._course_repo.get_all()


class GetCourseDetailUseCase:
    """Use case to fetch the detailed information of a single course."""

    def __init__(self, course_repo: CourseRepository):
        self._course_repo = course_repo

    def execute_by_slug(self, slug: str) -> Course:
        course = self._course_repo.get_by_slug(slug)
        if not course:
            raise CourseNotFoundError(slug)
        return course

    def execute_by_id(self, course_id: str) -> Course:
        course = self._course_repo.get_by_id(course_id)
        if not course:
            raise CourseNotFoundError(course_id)
        return course


class EnrollStudentUseCase:
    """Use case to validate and register a student for a specific course."""

    def __init__(self, course_repo: CourseRepository, enrollment_repo: EnrollmentRepository):
        self._course_repo = course_repo
        self._enrollment_repo = enrollment_repo

    def execute(self, request_dto: EnrollmentRequestDTO) -> EnrollmentResponseDTO:
        # Step 1: Preliminary DTO validation
        validation_errors = request_dto.validate()
        if validation_errors:
            return EnrollmentResponseDTO(
                success=False,
                message="Verifica los datos ingresados en el formulario.",
                errors=validation_errors
            )

        # Step 2: Course existence validation
        course = self._course_repo.get_by_slug(request_dto.course_slug)
        if not course:
            return EnrollmentResponseDTO(
                success=False,
                message=f"El curso seleccionado '{request_dto.course_slug}' no está disponible actualmente.",
                errors={"course": "Curso inexistente o cerrado"}
            )

        # Step 3: Instantiate domain entity and apply domain invariants
        try:
            enrollment = Enrollment(
                course_id=course.id,
                student_name=request_dto.student_name.strip(),
                student_email=request_dto.student_email.strip().lower(),
                student_phone=request_dto.student_phone.strip(),
                experience_level=request_dto.experience_level,
                comments=request_dto.comments.strip()
            )
            enrollment.validate()
        except InvalidEnrollmentError as err:
            return EnrollmentResponseDTO(
                success=False,
                message=str(err),
                errors=err.errors
            )

        # Step 4: Persist through port
        persisted = self._enrollment_repo.save(enrollment)

        return EnrollmentResponseDTO(
            success=True,
            message="¡Inscripción registrada exitosamente! Nos pondremos en contacto contigo a la brevedad.",
            enrollment_id=persisted.id,
            course_title=course.title,
            student_name=persisted.student_name,
            student_email=persisted.student_email,
            data={
                "enrollment": persisted.to_dict(),
                "course": course.to_dict()
            }
        )


class GetEnrollmentUseCase:
    """Use case to retrieve an enrollment by ID."""

    def __init__(self, enrollment_repo: EnrollmentRepository, course_repo: CourseRepository):
        self._enrollment_repo = enrollment_repo
        self._course_repo = course_repo

    def execute(self, enrollment_id: str) -> Optional[dict]:
        enrollment = self._enrollment_repo.get_by_id(enrollment_id)
        if not enrollment:
            return None
        course = self._course_repo.get_by_id(enrollment.course_id)
        return {
            "enrollment": enrollment,
            "course": course
        }


class GetInstructorProfileUseCase:
    """Use case providing information about Yoher Vazquez and stats."""

    def execute(self) -> Instructor:
        return Instructor()
