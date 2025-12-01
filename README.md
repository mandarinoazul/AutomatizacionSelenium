# Tarea 4: Pruebas Automatizadas con Selenium

Este proyecto consiste en la automatización de pruebas para el sistema de gestión de recursos humanos **OrangeHRM**, cubriendo flujos de Login y CRUD de usuarios.

## 📋 Información del Estudiante
* **Nombre:** Daniel E. Cabrera R.
* **Matrícula:** 2021-0554

## 🔗 Enlaces Obligatorios
> **Nota para el profesor:** Aquí están los accesos requeridos para la evaluación.

* **🎥 Video Demostrativo (YouTube):** [PEGA AQUÍ TU LINK DE YOUTUBE]
* **ticket Tablero de Gestión (Jira):** https://zohoidtsuport.atlassian.net/jira/software/projects/KAN/boards/1


## 🛠️ Tecnologías Utilizadas
* Python 3.x
* Selenium WebDriver
* Pytest
* Pytest-HTML (Reportes)
* WebDriver Manager

## 🚀 Cómo ejecutar las pruebas

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/mandarinoazul/AutomatizacionSelenium

   Instalar dependencias
   pip install -r requirements.txt

   Ejecutar pruebas y generar report
   py -m pytest test_proyecto.py --html=reporte_final.html --self-contained-html
