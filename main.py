"""Punto de entrada principal para el Aplicativo Web GUI en Flet con POO.

Evaluación Práctica - Programación IV
Instituto Universitario de Tecnología "Antonio José de Sucre"
Profesor: Yoher Alejandro Vazquez Salinas
"""
import os
import flet as ft
from src.gui.app import FletCoursesApp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COURSES_FILE = os.path.join(BASE_DIR, "data", "courses.json")
ENROLLMENTS_FILE = os.path.join(BASE_DIR, "data", "enrollments.json")


def main():
    # Instanciamos la aplicación POO
    app_controller = FletCoursesApp(
        courses_file=COURSES_FILE,
        enrollments_file=ENROLLMENTS_FILE
    )

    print("🚀 Iniciando Aplicativo Web GUI en Flet con POO...")
    print("📍 IUT 'Antonio José de Sucre' - Programación IV")
    print("👤 Docente: Yoher Alejandro Vazquez Salinas")
    print("🌐 Modo: Aplicación Web en Navegador (http://127.0.0.1:8550)")

    # Ejecutar la aplicación Flet directamente en el navegador web
    ft.run(
        app_controller.main,
        view=ft.AppView.WEB_BROWSER,
        host="127.0.0.1",
        port=8550
    )


if __name__ == "__main__":
    main()
