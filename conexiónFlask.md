En este apartado vamos a introducir el uso del framework Flask, un microframework de Python diseñado para el desarrollo de aplicaciones web y que
usaremos desde cPanel.

Para ello, tomaremos como base el repositorio:

https://github.com/jorgeenriquezm/jinja-hello-world

Este proyecto nos permite entender de forma sencilla cómo Flask utiliza el motor de plantillas Jinja para backend (Python) de la capa de presentación (HTML).

El repositorio presenta una estructura básica de Flask donde:

Python actúa como backend
Jinja gestiona las plantillas HTML
Se renderiza un archivo index.html dinámico

El punto clave es la función:

render_template("index.html")

Que indica a Flask que debe buscar el archivo HTML dentro de la carpeta:

/templates

El archivo index.html dentro de templates es la vista principal de la aplicación:

Es lo que ve el usuario al entrar en /

- Carpeta static (o public_html en cPanel) En local:

static/

En cPanel:

public_html/

CSS
JavaScript
Imágenes

Es contenido estático (no cambia dinámicamente)

Ejecución en local

Para ejecutar el proyecto en local necesitamos:

- Python instalado
- Flask instalado:
- pip install flask
+ Ejecución
- python app.py

Y Flask levanta un servidor local:

http://127.0.0.1:5000/

- Despliegue en cPanel

Cuando pasamos el proyecto a un servidor cPanel, la estructura cambia ligeramente.

- Configuración importante

En cPanel normalmente se usa:

Python App (Passenger WSGI)
Archivo de entrada: passenger_wsgi.py

Ejemplo:

from app import app as application

Diferencia clave: local vs servidor

Elemento	Local	cPanel

HTML	templates/	templates/

CSS/JS	static/	public_html/ o static/

Ejecución	python app.py	WSGI (Passenger)

URL	localhost	dominio real

Flujo de funcionamiento (Jinja)

El funcionamiento es el siguiente:

El usuario entra en la web

Flask ejecuta una ruta (/)

Python llama a render_template("index.html")

Jinja procesa el HTML

Se sustituyen variables dinámicas

Se devuelve HTML final al navegador

La conexión entre Jinja y flask

