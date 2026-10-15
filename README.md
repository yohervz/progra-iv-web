# Instituto Universitario de Tecnología "Antonio José de Sucre"
## Escuela de Informática — Asignatura: Programación IV (Tema III)
### Evaluación Práctica: Aplicativo Web GUI en Flet con Programación Orientada a Objetos (POO)

* **Docente Titular:** Ing. Yoher Alejandro Vazquez Salinas
* **Lapso Académico:** 2026-2 | **Corte:** I | **Ponderación:** 20%
* **Temática Desarrollada:** Plataforma Interactiva de Cursos de Tecnología (Inteligencia Artificial, Cloudflare y Cloud Computing)

---

## 📋 Resumen del Proyecto

Este proyecto consiste en un sistema interactivo web desarrollado con la biblioteca **Flet** y el lenguaje de programación **Python**, estructurado rigurosamente bajo los principios de la **Programación Orientada a Objetos (POO)** y arquitectura en capas. El aplicativo se ejecuta directamente en el **navegador web**, permitiendo explorar un catálogo de cursos especializados, consultar sus temarios y requisitos previos, registrar postulaciones de estudiantes mediante formularios validados y almacenar la información de forma persistente en archivos JSON.

---

## 🏛️ Arquitectura del Sistema y Diseño de Clases (POO)

El proyecto implementa una arquitectura desacoplada donde la lógica de negocio y las entidades son independientes de la capa de presentación:

```
progra/
├── data/                               # Persistencia de datos en formato JSON
│   ├── courses.json                    # Información, temarios y requisitos de cursos
│   └── enrollments.json                # Registro persistente de alumnos inscritos
├── src/
├── src/domain/                         # Capa de Dominio (Entidades de Negocio)
│   ├── entities.py                     # Clases Course, SyllabusModule, Enrollment, Instructor
│   ├── ports.py                        # Interfaces abstractas de repositorios
│   └── exceptions.py                   # Excepciones del dominio
├── src/application/                    # Capa de Aplicación (Casos de Uso)
│   ├── dtos.py                         # Clases EnrollmentRequestDTO, EnrollmentResponseDTO
│   └── use_cases.py                    # ListCoursesUseCase, EnrollStudentUseCase, etc.
├── src/infrastructure/                 # Capa de Infraestructura (Adaptadores)
│   └── repositories.py                 # JsonCourseRepository, JsonEnrollmentRepository
├── src/gui/                            # Capa de Presentación Web (Flet Web GUI)
│   ├── app.py                          # FletCoursesApp (Controlador central y ciclo de vida)
│   └── views.py                        # BaseView, HomeView, CoursesView, Detail, Form, Admin
├── tests/                              # Pruebas unitarias de POO y funcionalidad
│   ├── test_courses.py                 # Pruebas de dominio y casos de uso
│   └── test_flet_gui.py                # Pruebas de inicialización de componentes GUI
├── pyproject.toml                      # Definición de dependencias reproducibles
├── main.py                             # Punto de entrada de la aplicación Web GUI en Flet
└── README.md                           # Documentación técnica institucional
```

### Principios de Programación Orientada a Objetos Aplicados:
1. **Abstracción:** Se define la clase base abstracta `BaseView(ABC)` con el método `@abstractmethod build()`, obligando a que cada vista implemente su propia construcción de controles.
2. **Encapsulamiento:** Cada componente (como `CourseCardComponent` o `FletCoursesApp`) encapsula su estado interno y expone únicamente métodos públicos de interacción.
3. **Herencia:** Las vistas `HomeView`, `CoursesView`, `CourseDetailView`, `EnrollmentView`, `EnrollmentListView` y `AboutView` heredan de `BaseView`, reutilizando el acceso al ciclo de vida de la página y el manejador de navegación.
4. **Polimorfismo:** El método `navigate()` en `FletCoursesApp` despacha dinámicamente y renderiza la vista solicitada ejecutando `view_instance.build()` de forma polimórfica.
5. **Inyección de Dependencias:** Los casos de uso y repositorios se inyectan a través del constructor de las clases controladoras, evitando el acoplamiento rígido.

---

## 🚀 Guía de Instalación y Configuración con `uv`

Para garantizar la reproducibilidad requerida en la rúbrica, el entorno virtual se gestiona con la herramienta de alto rendimiento **`uv`**.

### 1. Requisitos Previos
* Python 3.10 o superior instalado en el sistema.
* Herramienta `uv` instalada.

### 2. Creación del Entorno Virtual con `uv`
Desde la raíz del proyecto, ejecuta:

```bash
# Crear el entorno virtual .venv
uv venv

# Activar el entorno virtual (macOS / Linux):
source .venv/bin/activate

# Activar el entorno virtual (Windows PowerShell):
# .venv\Scripts\Activate.ps1
```

### 3. Instalación de Dependencias con `uv`
Instala las bibliotecas requeridas (`flet`):

```bash
uv pip install flet
```

O instalando el proyecto mediante el archivo `pyproject.toml`:

```bash
uv pip install -e .
```

---

## 🌐 Instrucciones de Ejecución del Sistema Web

Para iniciar el servidor y abrir la aplicación interactiva en tu navegador web:

```bash
python run.py
```
*(O directamente mediante el intérprete del entorno virtual: `./.venv/bin/python main.py`)*

El sistema levantará el servidor web local y abrirá automáticamente la interfaz gráfica en:  
👉 **http://127.0.0.1:8550**

---

## 🕹️ Funcionalidades de la Interfaz Web Flet

1. **Pantalla de Inicio (Home):**
   - Banner de bienvenida con resumen formativo.
   - 4 tarjetas de estadísticas dinámicas del docente y la academia.
   - Destacados de cursos con acceso rápido al temario o inscripción.
2. **Catálogo de Cursos:**
   - Barra de búsqueda reactiva por título, tecnología o descripción.
   - Filtro desplegable por categoría (Inteligencia Artificial, Edge / Cloudflare, Cloud Computing).
   - Renderizado dinámico de tarjetas informativas.
3. **Ficha de Detalle del Curso:**
   - Visualización de la portada, precio y duración.
   - Lista estructurada de **Requisitos Previos** con iconos visuales.
   - **Temario / Plan de Estudios** desglosado por módulos y tópicos formativos.
4. **Formulario de Inscripción Personalizado:**
   - Campos de captura: Nombre, correo electrónico, teléfono/WhatsApp, nivel de experiencia y comentarios.
   - Validación reactiva POO (verifica longitud de campos, formato de correo electrónico y coherencia de datos).
   - Generación de código único de matrícula (`ENR-XXXXXX`) y confirmación visual con `AlertDialog`.
5. **Gestor de Inscritos (Base de Datos JSON):**
   - Tabla interactiva (`DataTable`) que consulta y lista todos los registros almacenados en `data/enrollments.json`.
6. **Módulo Institucional / Nosotros:**
   - Perfil profesional del profesor Ing. Yoher Alejandro Vazquez Salinas.
   - Credenciales del IUT "Antonio José de Sucre", cátedra de Programación IV y especialidades.

---

## 🧪 Ejecución de Pruebas Unitarias

El proyecto incluye pruebas automatizadas para verificar la arquitectura de datos y las vistas de la interfaz:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## 👨‍🏫 Información Institucional
* **Institución:** Instituto Universitario de Tecnología "Antonio José de Sucre"
* **Carrera:** Informática
* **Asignatura:** Programación IV — Sección A (Turno Diurno)
* **Profesor:** Yoher Alejandro Vazquez Salinas (info@yohervazquez.com)
