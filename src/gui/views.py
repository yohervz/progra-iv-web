"""Vistas y componentes Web GUI en Flet siguiendo Programación Orientada a Objetos (POO)."""
from abc import ABC, abstractmethod
from typing import Callable, Optional, List
import flet as ft

from ..domain.entities import Course, Enrollment, Instructor
from ..application.dtos import EnrollmentRequestDTO
from ..application.use_cases import (
    ListCoursesUseCase,
    GetCourseDetailUseCase,
    EnrollStudentUseCase,
    GetInstructorProfileUseCase
)
from ..infrastructure.repositories import JsonEnrollmentRepository


class BaseView(ABC):
    """Clase base abstracta para todas las vistas de la aplicación GUI (POO: Abstracción y Polimorfismo)."""

    def __init__(self, page: ft.Page, navigate_fn: Callable[[str, Optional[dict]], None]):
        self.page = page
        self.navigate = navigate_fn

    @abstractmethod
    def build(self) -> ft.Control:
        """Construye y retorna el árbol de controles de Flet para esta vista."""
        pass


class HomeView(BaseView):
    """Vista principal / Landing interactiva de la academia."""

    def __init__(
        self,
        page: ft.Page,
        navigate_fn: Callable[[str, Optional[dict]], None],
        list_courses_uc: ListCoursesUseCase,
        get_instructor_uc: GetInstructorProfileUseCase
    ):
        super().__init__(page, navigate_fn)
        self._list_courses_uc = list_courses_uc
        self._get_instructor_uc = get_instructor_uc

    def build(self) -> ft.Control:
        courses = self._list_courses_uc.execute()
        instructor = self._get_instructor_uc.execute()

        # Banner Hero
        hero_banner = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            "🎓 Academia de Tecnología & Cloud | Formación Especializada",
                            size=13,
                            weight=ft.FontWeight.W_600,
                            color="#93c5fd"
                        ),
                        bgcolor="#1e3a8a",
                        padding=8,
                        border_radius=20
                    ),
                    ft.Text(
                        "Domina la Inteligencia Artificial, Cloudflare y Cloud Computing",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color="#ffffff"
                    ),
                    ft.Text(
                        f"Programas prácticos e intensivos guiados por el {instructor.title} {instructor.name}. "
                        "Aprende con código limpio, arquitectura de software y proyectos reales.",
                        size=15,
                        color="#cbd5e1"
                    ),
                    ft.Row(
                        controls=[
                            ft.FilledButton(
                                content="Explorar Catálogo",
                                icon="rocket_launch",
                                on_click=lambda _: self.navigate("courses", None),
                                style=ft.ButtonStyle(bgcolor="#2563eb", color="#ffffff")
                            ),
                            ft.OutlinedButton(
                                content="Conocer al Docente",
                                icon="person",
                                on_click=lambda _: self.navigate("about", None),
                                style=ft.ButtonStyle(color="#ffffff")
                            )
                        ],
                        spacing=15
                    )
                ],
                spacing=16
            ),
            padding=30,
            border_radius=16,
            gradient=ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment.BOTTOM_RIGHT,
                colors=["#0f172a", "#1e1b4b", "#0f172a"]
            ),
            margin=10
        )

        # Estadísticas / Métricas clave (Componente POO Reutilizable)
        stats_row = ft.Row(
            controls=[
                self._build_stat_card("Alumnos Capacitados", instructor.stats.get("alumnos_capacitados", "+1,200"), "people", "#2563eb"),
                self._build_stat_card("Programas Dictados", instructor.stats.get("cursos_dictados", "18"), "menu_book", "#8b5cf6"),
                self._build_stat_card("Satisfacción Docente", instructor.stats.get("satisfaccion", "98%"), "thumb_up", "#10b981"),
                self._build_stat_card("Enfoque Práctico", "100% Proyectos", "code", "#f59e0b")
            ],
            spacing=15
        )

        # Cursos Destacados
        course_cards = [CourseCardComponent(course, self.navigate).build() for course in courses[:3]]

        return ft.ListView(
            controls=[
                hero_banner,
                stats_row,
                ft.Container(height=20),
                ft.Row(
                    controls=[
                        ft.Text("Cursos Disponibles", size=22, weight=ft.FontWeight.BOLD),
                        ft.TextButton("Ver todos", on_click=lambda _: self.navigate("courses", None))
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.ResponsiveRow(
                    controls=[ft.Column(col={"sm": 12, "md": 6, "lg": 4}, controls=[card]) for card in course_cards],
                    spacing=15
                ),
                ft.Container(height=30)
            ],
            spacing=15,
            expand=True
        )

    def _build_stat_card(self, title: str, value: str, icon_name: str, color_hex: str) -> ft.Control:
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icon_name, size=32, color=color_hex),
                    ft.Column(
                        controls=[
                            ft.Text(value, size=18, weight=ft.FontWeight.BOLD),
                            ft.Text(title, size=12, color="#64748b")
                        ],
                        spacing=2,
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=12
            ),
            bgcolor="#ffffff",
            padding=16,
            border_radius=12,
            border=ft.Border.all(1, "#e2e8f0"),
            expand=True
        )


class CourseCardComponent:
    """Componente reutilizable de tarjeta de curso (POO: Encapsulamiento y Composición)."""

    def __init__(self, course: Course, navigate_fn: Callable[[str, Optional[dict]], None]):
        self.course = course
        self.navigate = navigate_fn

    def build(self) -> ft.Control:
        badge_color = "#8b5cf6" if "Artificial" in self.course.category else ("#f97316" if "Cloudflare" in self.course.title else "#0ea5e9")

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Image(
                                src=self.course.cover_image,
                                height=150,
                                fit="cover",
                                border_radius=12
                            ),
                            margin=0
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Container(
                                                content=ft.Text(self.course.badge, size=11, color="#ffffff", weight=ft.FontWeight.BOLD),
                                                bgcolor=badge_color,
                                                padding=6,
                                                border_radius=6
                                            ),
                                            ft.Text(f"{self.course.duration}", size=12, color="#64748b")
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                    ),
                                    ft.Text(self.course.title, size=16, weight=ft.FontWeight.BOLD, max_lines=2),
                                    ft.Text(self.course.short_description, size=13, color="#475569", max_lines=3),
                                    ft.Divider(height=1, color="#e2e8f0"),
                                    ft.Row(
                                        controls=[
                                            ft.Column(
                                                controls=[
                                                    ft.Text("Inversión:", size=11, color="#64748b"),
                                                    ft.Text(self.course.formatted_price, size=16, weight=ft.FontWeight.BOLD, color="#0f172a")
                                                ],
                                                spacing=0
                                            ),
                                            ft.Row(
                                                controls=[
                                                    ft.OutlinedButton(
                                                        content="Temario",
                                                        on_click=lambda _: self.navigate("detail", {"slug": self.course.slug})
                                                    ),
                                                    ft.FilledButton(
                                                        content="Inscribirse",
                                                        on_click=lambda _: self.navigate("enroll", {"slug": self.course.slug}),
                                                        style=ft.ButtonStyle(bgcolor="#2563eb", color="#ffffff")
                                                    )
                                                ],
                                                spacing=8
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                    )
                                ],
                                spacing=10
                            ),
                            padding=16
                        )
                    ],
                    spacing=0
                ),
                padding=0
            ),
            elevation=2
        )


class CoursesView(BaseView):
    """Catálogo completo de cursos con barra de búsqueda y filtros reactivos."""

    def __init__(self, page: ft.Page, navigate_fn: Callable[[str, Optional[dict]], None], list_courses_uc: ListCoursesUseCase):
        super().__init__(page, navigate_fn)
        self._list_courses_uc = list_courses_uc
        self._all_courses: List[Course] = []
        self._filtered_courses: List[Course] = []
        self._grid_container = ft.ResponsiveRow(spacing=15)
        self._search_input = ft.TextField(
            hint_text="Buscar curso por título, tecnología o palabras clave...",
            prefix_icon="search",
            expand=True,
            on_change=self._on_search_change
        )
        self._filter_dropdown = ft.Dropdown(
            label="Categoría",
            width=220,
            value="Todas",
            options=[
                ft.dropdown.Option("Todas"),
                ft.dropdown.Option("Inteligencia Artificial"),
                ft.dropdown.Option("Edge & Seguridad Web"),
                ft.dropdown.Option("Cloud Computing")
            ],
            on_select=self._on_filter_change
        )

    def build(self) -> ft.Control:
        self._all_courses = self._list_courses_uc.execute()
        self._filtered_courses = list(self._all_courses)
        self._render_cards()

        return ft.Column(
            controls=[
                ft.Text("Catálogo Oficial de Cursos", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Selecciona un programa para ver sus requisitos, módulos formativos e inscribirte.", size=14, color="#64748b"),
                ft.Row(controls=[self._search_input, self._filter_dropdown], spacing=15),
                ft.Divider(height=1, color="#e2e8f0"),
                self._grid_container
            ],
            spacing=15,
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )

    def _render_cards(self):
        self._grid_container.controls = [
            ft.Column(col={"sm": 12, "md": 6, "lg": 4}, controls=[CourseCardComponent(c, self.navigate).build()])
            for c in self._filtered_courses
        ]
        if not self._filtered_courses:
            self._grid_container.controls = [
                ft.Container(
                    content=ft.Text("No se encontraron cursos que coincidan con la búsqueda.", size=15, color="#64748b"),
                    padding=30
                )
            ]

    def _on_search_change(self, e):
        query = (self._search_input.value or "").strip().lower()
        category = self._filter_dropdown.value
        self._apply_filters(query, category)

    def _on_filter_change(self, e):
        query = (self._search_input.value or "").strip().lower()
        category = self._filter_dropdown.value
        self._apply_filters(query, category)

    def _apply_filters(self, query: str, category: str):
        self._filtered_courses = [
            c for c in self._all_courses
            if (category == "Todas" or c.category == category)
            and (not query or query in c.title.lower() or query in c.short_description.lower() or any(query in t.lower() for t in c.tags))
        ]
        self._render_cards()
        if self.page:
            self.page.update()


class CourseDetailView(BaseView):
    """Detalle completo del curso: temario estructurado, requisitos e inscripción."""

    def __init__(self, page: ft.Page, navigate_fn: Callable[[str, Optional[dict]], None], get_course_detail_uc: GetCourseDetailUseCase, slug: str):
        super().__init__(page, navigate_fn)
        self._get_course_detail_uc = get_course_detail_uc
        self.slug = slug

    def build(self) -> ft.Control:
        course = self._get_course_detail_uc.execute_by_slug(self.slug)

        # Requisitos con iconos
        requirements_controls = [
            ft.Row(
                controls=[
                    ft.Icon("check_circle", color="#10b981", size=18),
                    ft.Text(req, size=14, color="#334155", expand=True)
                ],
                spacing=10
            ) for req in course.requirements
        ]

        # Temario por Módulos
        syllabus_controls = []
        for i, mod in enumerate(course.syllabus, start=1):
            topics_list = [
                ft.Row(
                    controls=[
                        ft.Icon("arrow_forward", color="#2563eb", size=16),
                        ft.Text(topic, size=13, color="#475569", expand=True)
                    ],
                    spacing=6
                ) for topic in mod.topics
            ]
            syllabus_controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(mod.module, size=15, weight=ft.FontWeight.BOLD, color="#1e293b"),
                            ft.Column(controls=topics_list, spacing=4)
                        ],
                        spacing=8
                    ),
                    bgcolor="#f8fafc",
                    padding=12,
                    border_radius=8,
                    border=ft.Border.all(1, "#e2e8f0"),
                    margin=4
                )
            )

        return ft.ListView(
            controls=[
                ft.TextButton("← Volver a Cursos", on_click=lambda _: self.navigate("courses", None)),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Image(src=course.cover_image, width=320, height=200, fit="cover", border_radius=12),
                            ft.Column(
                                controls=[
                                    ft.Text(course.category.upper(), size=12, color="#2563eb", weight=ft.FontWeight.BOLD),
                                    ft.Text(course.title, size=24, weight=ft.FontWeight.BOLD, expand=True),
                                    ft.Text(course.subtitle, size=14, color="#64748b"),
                                    ft.Row(
                                        controls=[
                                            ft.Text(f"⏱ Duración: {course.duration}", size=13),
                                            ft.Text(f"📊 Nivel: {course.level}", size=13),
                                            ft.Text(f"👨‍🏫 Docente: {course.instructor_name}", size=13),
                                        ],
                                        spacing=20
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.Text(f"Inversión: {course.formatted_price}", size=20, weight=ft.FontWeight.BOLD, color="#0f172a"),
                                            ft.FilledButton(
                                                content="Inscribirme Ahora",
                                                icon="app_registration",
                                                on_click=lambda _: self.navigate("enroll", {"slug": course.slug}),
                                                style=ft.ButtonStyle(bgcolor="#2563eb", color="#ffffff")
                                            )
                                        ],
                                        spacing=20
                                    )
                                ],
                                spacing=10,
                                expand=True
                            )
                        ],
                        spacing=20,
                        vertical_alignment=ft.CrossAxisAlignment.START
                    ),
                    padding=20,
                    bgcolor="#ffffff",
                    border_radius=12,
                    border=ft.Border.all(1, "#e2e8f0")
                ),
                ft.Container(height=10),
                ft.Text("Descripción General del Programa", size=18, weight=ft.FontWeight.BOLD),
                ft.Text(course.full_description, size=15, color="#334155"),
                ft.Container(height=10),
                ft.Text("Requisitos Previos", size=18, weight=ft.FontWeight.BOLD),
                ft.Column(controls=requirements_controls, spacing=8),
                ft.Container(height=10),
                ft.Text("Plan de Estudios / Temario", size=18, weight=ft.FontWeight.BOLD),
                ft.Column(controls=syllabus_controls, spacing=8),
                ft.Container(height=20)
            ],
            spacing=15,
            expand=True
        )


class EnrollmentView(BaseView):
    """Formulario interactivo de inscripción con validación POO y persistencia en JSON."""

    def __init__(
        self,
        page: ft.Page,
        navigate_fn: Callable[[str, Optional[dict]], None],
        get_course_detail_uc: GetCourseDetailUseCase,
        enroll_student_uc: EnrollStudentUseCase,
        slug: str
    ):
        super().__init__(page, navigate_fn)
        self._get_course_detail_uc = get_course_detail_uc
        self._enroll_student_uc = enroll_student_uc
        self.slug = slug

        # Controles de formulario
        self.name_field = ft.TextField(label="Nombre Completo *", hint_text="Ej. Pedro Pérez", expand=True)
        self.email_field = ft.TextField(label="Correo Electrónico *", hint_text="ejemplo@correo.com", expand=True)
        self.phone_field = ft.TextField(label="Teléfono / WhatsApp *", hint_text="+58 412 1234567", expand=True)
        self.level_dropdown = ft.Dropdown(
            label="Nivel de Experiencia",
            value="Principiante",
            options=[
                ft.dropdown.Option("Principiante"),
                ft.dropdown.Option("Intermedio"),
                ft.dropdown.Option("Avanzado")
            ],
            expand=True
        )
        self.comments_field = ft.TextField(
            label="Expectativas o comentarios (Opcional)",
            multiline=True,
            min_lines=2,
            max_lines=4,
            expand=True
        )
        self.error_banner = ft.Text("", color="#ef4444", size=13, weight=ft.FontWeight.BOLD, visible=False)

    def build(self) -> ft.Control:
        course = self._get_course_detail_uc.execute_by_slug(self.slug)

        return ft.ListView(
            controls=[
                ft.TextButton("← Volver", on_click=lambda _: self.navigate("detail", {"slug": self.slug})),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(f"Inscripción al Curso: {course.title}", size=22, weight=ft.FontWeight.BOLD),
                            ft.Text(f"Inversión: {course.formatted_price} | Duración: {course.duration}", size=14, color="#64748b"),
                            ft.Divider(color="#e2e8f0"),
                            self.error_banner,
                            self.name_field,
                            ft.Row(controls=[self.email_field, self.phone_field], spacing=15),
                            self.level_dropdown,
                            self.comments_field,
                            ft.FilledButton(
                                content="Confirmar y Registrar Inscripción",
                                icon="check_circle",
                                on_click=self._submit_enrollment,
                                style=ft.ButtonStyle(bgcolor="#2563eb", color="#ffffff")
                            )
                        ],
                        spacing=15
                    ),
                    padding=25,
                    bgcolor="#ffffff",
                    border_radius=12,
                    border=ft.Border.all(1, "#e2e8f0"),
                    width=750
                )
            ],
            spacing=15,
            expand=True
        )

    def _submit_enrollment(self, e):
        # DTO de solicitud POO
        dto = EnrollmentRequestDTO(
            course_slug=self.slug,
            student_name=self.name_field.value or "",
            student_email=self.email_field.value or "",
            student_phone=self.phone_field.value or "",
            experience_level=self.level_dropdown.value or "Principiante",
            comments=self.comments_field.value or ""
        )

        response = self._enroll_student_uc.execute(dto)

        if not response.success:
            err_msg = response.message
            if response.errors:
                err_msg += " " + " | ".join(response.errors.values())
            self.error_banner.value = f"⚠️ {err_msg}"
            self.error_banner.visible = True
            if self.page:
                self.page.update()
            return

        # Modal de éxito
        dialog = ft.AlertDialog(
            title=ft.Text("¡Inscripción Exitosa!"),
            content=ft.Text(
                f"Estudiante: {response.student_name}\n"
                f"Código de Matrícula: {response.enrollment_id}\n\n"
                f"Se han guardado los datos exitosamente en el repositorio JSON.",
                size=14
            ),
            actions=[
                ft.FilledButton("Ir a Mis Inscripciones", on_click=lambda _: self._close_dialog_and_navigate(dialog, "enrollments")),
                ft.OutlinedButton("Volver al Catálogo", on_click=lambda _: self._close_dialog_and_navigate(dialog, "courses"))
            ]
        )
        if self.page:
            self.page.overlay.append(dialog)
            dialog.open = True
            self.page.update()

    def _close_dialog_and_navigate(self, dialog: ft.AlertDialog, target_route: str):
        dialog.open = False
        if self.page:
            self.page.update()
        self.navigate(target_route, None)


class EnrollmentListView(BaseView):
    """Gestión y consulta interactiva de inscritos almacenados en JSON."""

    def __init__(self, page: ft.Page, navigate_fn: Callable[[str, Optional[dict]], None], enrollment_repo: JsonEnrollmentRepository):
        super().__init__(page, navigate_fn)
        self._enrollment_repo = enrollment_repo

    def build(self) -> ft.Control:
        all_raw = self._enrollment_repo._read_data()
        records = [Enrollment.from_dict(r) for r in all_raw]

        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(rec.id, weight=ft.FontWeight.BOLD)),
                    ft.DataCell(ft.Text(rec.student_name)),
                    ft.DataCell(ft.Text(rec.student_email)),
                    ft.DataCell(ft.Text(rec.student_phone)),
                    ft.DataCell(ft.Text(rec.experience_level)),
                    ft.DataCell(ft.Text(rec.course_id))
                ]
            ) for rec in records
        ]

        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Código")),
                ft.DataColumn(ft.Text("Estudiante")),
                ft.DataColumn(ft.Text("Correo")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Nivel")),
                ft.DataColumn(ft.Text("ID Curso"))
            ],
            rows=rows
        )

        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Registro de Inscripciones Activas (JSON)", size=22, weight=ft.FontWeight.BOLD),
                        ft.FilledButton("Inscribir Nuevo Alumno", icon="add", on_click=lambda _: self.navigate("courses", None))
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Text(f"Total de postulaciones registradas en base de datos JSON: {len(records)}", size=14, color="#64748b"),
                ft.Divider(color="#e2e8f0"),
                ft.Container(
                    content=ft.Column(controls=[table], scroll=ft.ScrollMode.AUTO),
                    bgcolor="#ffffff",
                    padding=16,
                    border_radius=12,
                    border=ft.Border.all(1, "#e2e8f0"),
                    expand=True
                )
            ],
            spacing=15,
            expand=True
        )


class AboutView(BaseView):
    """Perfil del docente e información institucional de Programación IV."""

    def __init__(self, page: ft.Page, navigate_fn: Callable[[str, Optional[dict]], None], get_instructor_uc: GetInstructorProfileUseCase):
        super().__init__(page, navigate_fn)
        self._get_instructor_uc = get_instructor_uc

    def build(self) -> ft.Control:
        instructor = self._get_instructor_uc.execute()

        specialties_chips = [
            ft.Chip(label=ft.Text(spec), bgcolor="#f1f5f9") for spec in instructor.specialties
        ]

        return ft.ListView(
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Image(
                                src=instructor.avatar_url,
                                width=140,
                                height=140,
                                fit="cover",
                                border_radius=70
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(instructor.name, size=24, weight=ft.FontWeight.BOLD),
                                    ft.Text(instructor.title, size=15, color="#2563eb", weight=ft.FontWeight.W_600),
                                    ft.Text("Instituto Universitario de Tecnología 'Antonio José de Sucre'", size=13, color="#64748b"),
                                    ft.Text("Asignatura: Programación IV | Cátedra de Informática", size=13, color="#64748b"),
                                    ft.Text("📧 info@yohervazquez.com", size=13, weight=ft.FontWeight.BOLD)
                                ],
                                spacing=4,
                                expand=True
                            )
                        ],
                        spacing=25,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    bgcolor="#ffffff",
                    padding=25,
                    border_radius=16,
                    border=ft.Border.all(1, "#e2e8f0")
                ),
                ft.Container(height=10),
                ft.Text("Trayectoria y Visión Académica", size=18, weight=ft.FontWeight.BOLD),
                ft.Text(instructor.bio, size=15, color="#334155"),
                ft.Container(
                    content=ft.Text(f'"{instructor.teaching_philosophy}"', italic=True, size=14, color="#1e3a8a"),
                    bgcolor="#eff6ff",
                    padding=16,
                    border_radius=8,
                    border=ft.Border.all(1, "#bfdbfe")
                ),
                ft.Container(height=10),
                ft.Text("Áreas de Especialización", size=18, weight=ft.FontWeight.BOLD),
                ft.Row(controls=specialties_chips, wrap=True, spacing=8)
            ],
            spacing=15,
            expand=True
        )
