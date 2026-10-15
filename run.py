"""Entrypoint for launching the Flask courses application."""
from src.web.app import create_app

app = create_app()

if __name__ == "__main__":
    print("🚀 Servidor de Cursos de IA & Cloud iniciado en http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
