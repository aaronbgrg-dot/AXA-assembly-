# 🐍 Generic Jinja Server & Hello World

Este proyecto es un servidor web minimalista basado en **Python** y **Flask** que permite utilizar el motor de plantillas **Jinja2** directamente en archivos HTML. Está diseñado especialmente para entornos educativos o prototipado rápido donde se busca una experiencia similar a PHP pero con la potencia de Python.

## 🚀 Características

- **Servidor Genérico**: No necesitas configurar rutas. Cualquier archivo `.html` en la raíz será renderizado automáticamente.
- **Lógica en HTML**: Permite a los alumnos practicar lógica de programación (`if`, `for`, `set`) directamente dentro del HTML.
- **Diseño Premium**: Incluye un ejemplo de "Hello World" con una interfaz moderna basada en *Glassmorphism*.
- **Listo para Producción**: Incluye configuración para despliegue en servidores cPanel/Passenger.

## 🛠️ Instalación Local

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/tu-repo.git
   cd tu-repo
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar el servidor**:
   ```bash
   python app.py
   ```

4. **Acceder**:
   Abre [http://127.0.0.1:5000](http://127.0.0.1:5000) en tu navegador.

## 📂 Estructura del Proyecto

- `app.py`: El núcleo del servidor Flask que gestiona el renderizado dinámico.
- `index.html`: Plantilla principal de ejemplo con lógica de Jinja.
- `passenger_wsgi.py`: Archivo de configuración para despliegue en hosting compartido (cPanel).
- `requirements.txt`: Lista de librerías necesarias.

## 🌐 Despliegue (cPanel)

Para desplegar en cPanel, asegúrate de configurar el **Application startup file** como `passenger_wsgi.py` y el **Application Entry point** como `application`. Para más detalles, consulta la [Guía de Instalación](GUIA_CPANEL.md).

---
Desarrollado para fines educativos. 🎓
