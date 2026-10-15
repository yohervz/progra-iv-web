"""Data Transfer Objects (DTOs) for the Application layer."""
from dataclasses import dataclass
from typing import Optional, Dict, Any, List


@dataclass
class EnrollmentRequestDTO:
    """Incoming request payload for enrolling into a course."""
    course_slug: str
    student_name: str
    student_email: str
    student_phone: str
    experience_level: str
    comments: str = ""

    def validate(self) -> Dict[str, str]:
        """Performs initial request-level validation."""
        errors = {}
        if not self.student_name or len(self.student_name.strip()) < 3:
            errors["student_name"] = "Por favor ingresa tu nombre y apellido (mínimo 3 caracteres)."

        if not self.student_email or "@" not in self.student_email or "." not in self.student_email:
            errors["student_email"] = "Por favor ingresa una dirección de correo electrónico válida."

        if not self.student_phone or len(self.student_phone.strip()) < 7:
            errors["student_phone"] = "Por favor ingresa un número de teléfono o WhatsApp válido."

        if not self.course_slug:
            errors["course_slug"] = "Curso no especificado."

        return errors


@dataclass
class EnrollmentResponseDTO:
    """Outgoing response returned by the enrollment use case."""
    success: bool
    message: str
    enrollment_id: Optional[str] = None
    course_title: Optional[str] = None
    student_name: Optional[str] = None
    student_email: Optional[str] = None
    errors: Optional[Dict[str, str]] = None
    data: Optional[Dict[str, Any]] = None
