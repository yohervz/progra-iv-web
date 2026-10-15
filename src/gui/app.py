"""Controlador y contenedor principal de la aplicación Web GUI en Flet con POO."""
import os
from typing import Optional, Dict, Any
import flet as ft

from ..infrastructure.repositories import JsonCourseRepository, JsonEnrollmentRepository
from ..application.use_cases import (
    ListCoursesUseCase,
    GetCourseDetailUseCase,
    EnrollStudentUseCase,
    GetEnrollmentUseCase,
    GetInstructorProfileUseCase
)
from .views import HomeView, CoursesView, CourseDetailView, EnrollmentView, EnrollmentListView, AboutView


class FletCoursesApp:
    """Clase principal que encapsula el estado, navegación y ciclo de vida de la Web GUI Flet (POO)."""

    def __init__(self, courses_file: str, enrollments_file: str):
        # 1. Repositorios de infraestructura
        self.course_repo = JsonCourseRepository(courses_file)
        self.enrollment_repo = JsonEnrollmentRepository(enrollments_file)

        # 2. Casos de uso de la capa de aplicación
        self.list_courses_uc = ListCoursesUseCase(self.course_repo)
        self.get_course_detail_uc = GetCourseDetailUseCase(self.course_repo)
        self.enroll_student_uc = EnrollStudentUseCase(self.course_repo, self.enrollment_repo)
        self.get_enrollment_uc = GetEnrollmentUseCase(self.enrollment_repo, self.course_repo)
        self.get_instructor_uc = GetInstructorProfileUseCase()

        # 3. Referencia a la página y contenedor dinámico
        self.page: Optional[ft.Page] = None
        self.nav_rail: Optional[ft.NavigationRail] = None
        self.content_area = ft.Container(expand=True, padding=20)
        self.current_route: str = "home"
        self.route_params: Optional[Dict[str, Any]] = None

    def main(self, page: ft.Page):
        """Punto de entrada de Flet al inicializar la sesión web."""
        self.page = page
        self.page.title = "IUT Antonio José de Sucre - Programación IV | Plataforma Tech en Flet"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.bgcolor = "#f8fafc"
        self.page.padding = 0

        # Barra de navegación lateral (NavigationRail)
        self.nav_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=80,
            min_extended_width=200,
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon="home_outlined",
                    selected_icon="home",
                    label="Inicio"
                ),
                ft.NavigationRailDestination(
                    icon="menu_book_outlined",
                    selected_icon="menu_book",
                    label="Cursos"
                ),
                ft.NavigationRailDestination(
                    icon="how_to_reg_outlined",
                    selected_icon="how_to_reg",
                    label="Inscritos"
                ),
                ft.NavigationRailDestination(
                    icon="person_outlined",
                    selected_icon="person",
                    label="Docente"
                ),
            ],
            on_change=self._on_nav_change,
            bgcolor="#ffffff"
        )

        # Barra superior AppBar
        self.page.appbar = ft.AppBar(
            title=ft.Row(
                controls=[
                    ft.Icon("school", color="#ffffff"),
                    ft.Column(
                        controls=[
                            ft.Text("IUT 'Antonio José de Sucre' — Programación IV", size=16, weight=ft.FontWeight.BOLD, color="#ffffff"),
                            ft.Text("Evaluación Práctica: Aplicativo Web GUI en Flet con POO | Prof. Yoher Alejandro Vazquez Salinas", size=11, color="#cbd5e1")
                        ],
                        spacing=0
                    )
                ],
                spacing=10
            ),
            bgcolor="#0f172a",
            center_title=False
        )

        # Disposición principal en fila
        body = ft.Row(
            controls=[
                self.nav_rail,
                ft.VerticalDivider(width=1, color="#e2e8f0"),
                self.content_area
            ],
            expand=True,
            spacing=0
        )

        self.page.add(body)
        self.navigate("home")

    def _on_nav_change(self, e):
        idx = e.control.selected_index
        route_map = {0: "home", 1: "courses", 2: "enrollments", 3: "about"}
        target = route_map.get(idx, "home")
        self.navigate(target)

    def navigate(self, route_name: str, params: Optional[Dict[str, Any]] = None):
        """Manejador centralizado de navegación reactiva en Flet."""
        self.current_route = route_name
        self.route_params = params or {}

        # Sincronizar índice visual del nav_rail
        if self.nav_rail:
            if route_name in ["home"]:
                self.nav_rail.selected_index = 0
            elif route_name in ["courses", "detail", "enroll"]:
                self.nav_rail.selected_index = 1
            elif route_name in ["enrollments"]:
                self.nav_rail.selected_index = 2
            elif route_name in ["about"]:
                self.nav_rail.selected_index = 3

        # Instanciar la vista correspondiente aplicando Polimorfismo
        view_instance = None
        if route_name == "home":
            view_instance = HomeView(self.page, self.navigate, self.list_courses_uc, self.get_instructor_uc)
        elif route_name == "courses":
            view_instance = CoursesView(self.page, self.navigate, self.list_courses_uc)
        elif route_name == "detail":
            slug = self.route_params.get("slug", "")
            view_instance = CourseDetailView(self.page, self.navigate, self.get_course_detail_uc, slug)
        elif route_name == "enroll":
            slug = self.route_params.get("slug", "")
            view_instance = EnrollmentView(self.page, self.navigate, self.get_course_detail_uc, self.enroll_student_uc, slug)
        elif route_name == "enrollments":
            view_instance = EnrollmentListView(self.page, self.navigate, self.enrollment_repo)
        elif route_name == "about":
            view_instance = AboutView(self.page, self.navigate, self.get_instructor_uc)

        if view_instance:
            self.content_area.content = view_instance.build()
            if self.page:
                self.page.update()
