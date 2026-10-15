"""Domain ports specifying interfaces for repositories and external adapters."""
from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Course, Enrollment


class CourseRepository(ABC):
    """Abstract port for querying course data."""

    @abstractmethod
    def get_all(self) -> List[Course]:
        """Retrieve all available courses."""
        pass

    @abstractmethod
    def get_by_id(self, course_id: str) -> Optional[Course]:
        """Retrieve a specific course by its unique ID."""
        pass

    @abstractmethod
    def get_by_slug(self, slug: str) -> Optional[Course]:
        """Retrieve a specific course by its URL slug."""
        pass


class EnrollmentRepository(ABC):
    """Abstract port for managing course student enrollments."""

    @abstractmethod
    def save(self, enrollment: Enrollment) -> Enrollment:
        """Persist a newly created enrollment."""
        pass

    @abstractmethod
    def get_by_id(self, enrollment_id: str) -> Optional[Enrollment]:
        """Retrieve an enrollment record by its unique ID."""
        pass

    @abstractmethod
    def get_by_course(self, course_id: str) -> List[Enrollment]:
        """Retrieve all enrollments associated with a specific course."""
        pass
