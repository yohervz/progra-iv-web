"""Domain entities adhering to Object-Oriented Programming (OOP) principles."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
import re
import uuid
from typing import List, Dict, Any
from .exceptions import InvalidEnrollmentError


@dataclass
class SyllabusModule:
    """Represents a module in the course curriculum."""
    module: str
    topics: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SyllabusModule":
        return cls(
            module=data.get("module", ""),
            topics=list(data.get("topics", []))
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "module": self.module,
            "topics": self.topics
        }


@dataclass
class Course:
    """Course domain entity representing an educational offering."""
    id: str
    slug: str
    title: str
    subtitle: str
    category: str
    level: str
    duration: str
    price: float
    currency: str
    badge: str
    cover_image: str
    instructor_name: str
    short_description: str
    full_description: str
    requirements: List[str] = field(default_factory=list)
    syllabus: List[SyllabusModule] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    @property
    def formatted_price(self) -> str:
        """Returns the price formatted with currency symbol."""
        if self.price == 0:
            return "Gratuito"
        return f"${self.price:,.2f} {self.currency}"

    @property
    def is_free(self) -> bool:
        """Determines whether the course is free of charge."""
        return self.price <= 0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Course":
        """Factory method creating a Course entity from a dictionary."""
        raw_syllabus = data.get("syllabus", [])
        parsed_syllabus = [
            SyllabusModule.from_dict(m) if isinstance(m, dict) else m
            for m in raw_syllabus
        ]
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            slug=data.get("slug", ""),
            title=data.get("title", ""),
            subtitle=data.get("subtitle", ""),
            category=data.get("category", "General"),
            level=data.get("level", "Todos los niveles"),
            duration=data.get("duration", "4 semanas"),
            price=float(data.get("price", 0.0)),
            currency=data.get("currency", "USD"),
            badge=data.get("badge", ""),
            cover_image=data.get("cover_image", ""),
            instructor_name=data.get("instructor_name", "Yoher Vazquez"),
            short_description=data.get("short_description", ""),
            full_description=data.get("full_description", ""),
            requirements=list(data.get("requirements", [])),
            syllabus=parsed_syllabus,
            tags=list(data.get("tags", []))
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the course entity into a dictionary."""
        return {
            "id": self.id,
            "slug": self.slug,
            "title": self.title,
            "subtitle": self.subtitle,
            "category": self.category,
            "level": self.level,
            "duration": self.duration,
            "price": self.price,
            "currency": self.currency,
            "badge": self.badge,
            "cover_image": self.cover_image,
            "instructor_name": self.instructor_name,
            "short_description": self.short_description,
            "full_description": self.full_description,
            "requirements": self.requirements,
            "syllabus": [m.to_dict() for m in self.syllabus],
            "tags": self.tags
        }


@dataclass
class Enrollment:
    """Enrollment entity representing a student application to a course."""
    course_id: str
    student_name: str
    student_email: str
    student_phone: str
    experience_level: str
    comments: str = ""
    id: str = field(default_factory=lambda: f"ENR-{uuid.uuid4().hex[:8].upper()}")
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def validate(self) -> None:
        """Enforces domain integrity rules on enrollment data."""
        errors: Dict[str, str] = {}

        if not self.student_name or len(self.student_name.strip()) < 3:
            errors["student_name"] = "El nombre completo debe tener al menos 3 caracteres."

        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not self.student_email or not re.match(email_pattern, self.student_email.strip()):
            errors["student_email"] = "Por favor ingresa un correo electrónico válido."

        if not self.student_phone or len(self.student_phone.strip()) < 7:
            errors["student_phone"] = "Ingresa un número telefónico o WhatsApp de contacto válido."

        if not self.course_id:
            errors["course_id"] = "El identificador del curso es obligatorio."

        if errors:
            raise InvalidEnrollmentError("Datos de inscripción inválidos.", errors=errors)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Enrollment":
        return cls(
            id=data.get("id", f"ENR-{uuid.uuid4().hex[:8].upper()}"),
            course_id=data.get("course_id", ""),
            student_name=data.get("student_name", ""),
            student_email=data.get("student_email", ""),
            student_phone=data.get("student_phone", ""),
            experience_level=data.get("experience_level", "Principiante"),
            comments=data.get("comments", ""),
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat())
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "course_id": self.course_id,
            "student_name": self.student_name,
            "student_email": self.student_email,
            "student_phone": self.student_phone,
            "experience_level": self.experience_level,
            "comments": self.comments,
            "created_at": self.created_at
        }


@dataclass
class Instructor:
    """Entity representing the course instructor and author profile."""
    name: str = "Yoher Vazquez"
    title: str = "Ingeniero en Informática & Docente Universitario"
    bio: str = (
        "Especialista en desarrollo de software, inteligencia artificial aplicada, "
        "infraestructura en la nube y optimización perimetral (Edge). Cuenta con amplia "
        "experiencia académica y profesional preparando a desarrolladores e ingenieros para "
        "enfrentar desafíos tecnológicos modernos con excelencia técnica y proyectos reales."
    )
    teaching_philosophy: str = (
        "Aprender haciendo: proyectos reales con diseño robusto, código limpio y "
        "despliegues prácticos desde la primera semana."
    )
    experience_years: int = 10
    specialties: List[str] = field(default_factory=lambda: [
        "Inteligencia Artificial y LLMs",
        "Cloudflare & Edge Computing",
        "Cloud Computing (AWS / GCP)",
        "Ingeniería de Software & Arquitectura de Sistemas",
        "Soluciones Prácticas y Escalables"
    ])
    avatar_url: str = "https://yohervazquez.com/images/personal/yoher-vazquez.png"
    stats: Dict[str, Any] = field(default_factory=lambda: {
        "alumnos_capacitados": "+1,200",
        "cursos_dictados": "18",
        "satisfaccion": "98%",
        "proyectos_asesorados": "+60"
    })

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "title": self.title,
            "bio": self.bio,
            "teaching_philosophy": self.teaching_philosophy,
            "experience_years": self.experience_years,
            "specialties": self.specialties,
            "avatar_url": self.avatar_url,
            "stats": self.stats
        }
