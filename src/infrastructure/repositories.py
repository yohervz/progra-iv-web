"""Infrastructure adapters: Concrete repositories persisting and loading data from JSON files."""
import json
import os
import threading
from typing import List, Optional
from ..domain.entities import Course, Enrollment
from ..domain.ports import CourseRepository, EnrollmentRepository


class JsonCourseRepository(CourseRepository):
    """Adapter reading Course entities from a JSON data source."""

    def __init__(self, file_path: str):
        self._file_path = file_path
        self._lock = threading.Lock()

    def _read_data(self) -> List[dict]:
        if not os.path.exists(self._file_path):
            return []
        try:
            with open(self._file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def get_all(self) -> List[Course]:
        with self._lock:
            raw_list = self._read_data()
            return [Course.from_dict(item) for item in raw_list]

    def get_by_id(self, course_id: str) -> Optional[Course]:
        courses = self.get_all()
        for course in courses:
            if course.id == course_id:
                return course
        return None

    def get_by_slug(self, slug: str) -> Optional[Course]:
        courses = self.get_all()
        for course in courses:
            if course.slug.lower() == slug.lower():
                return course
        return None


class JsonEnrollmentRepository(EnrollmentRepository):
    """Adapter persisting and retrieving Enrollment entities to a JSON file."""

    def __init__(self, file_path: str):
        self._file_path = file_path
        self._lock = threading.Lock()
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        os.makedirs(os.path.dirname(os.path.abspath(self._file_path)), exist_ok=True)
        if not os.path.exists(self._file_path):
            with open(self._file_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _read_data(self) -> List[dict]:
        if not os.path.exists(self._file_path):
            return []
        try:
            with open(self._file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def _write_data(self, data: List[dict]) -> None:
        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def save(self, enrollment: Enrollment) -> Enrollment:
        with self._lock:
            records = self._read_data()
            # Check if updating an existing record or appending a new one
            updated = False
            for i, rec in enumerate(records):
                if rec.get("id") == enrollment.id:
                    records[i] = enrollment.to_dict()
                    updated = True
                    break
            if not updated:
                records.append(enrollment.to_dict())
            self._write_data(records)
            return enrollment

    def get_by_id(self, enrollment_id: str) -> Optional[Enrollment]:
        with self._lock:
            records = self._read_data()
            for rec in records:
                if rec.get("id") == enrollment_id:
                    return Enrollment.from_dict(rec)
            return None

    def get_by_course(self, course_id: str) -> List[Enrollment]:
        with self._lock:
            records = self._read_data()
            return [
                Enrollment.from_dict(rec)
                for rec in records
                if rec.get("course_id") == course_id
            ]
