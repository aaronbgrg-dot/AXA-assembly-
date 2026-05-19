from flask import Flask, render_template_string, request, abort
import os

app = Flask(__name__)

# Este servidor busca cualquier archivo .html en la carpeta y lo renderiza con Jinja
@app.route('/')
@app.route('/<path:filename>')
def serve_any_html(filename='index.html'):
    # Si la ruta termina en / (como la raíz), buscamos index.html
    if filename.endswith('/') or not filename:
        filename += 'index.html'
    
    # Si no tiene extensión, le ponemos .html
    if '.' not in filename:
        filename += '.html'

    if os.path.exists(filename) and filename.endswith('.html'):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                template_content = f.read()
            # Renderizamos permitiendo lógica de Jinja en el HTML
            return render_template_string(template_content, request=request)
        except Exception as e:
            return f"Error al procesar el archivo: {e}", 500
    else:
        return f"El archivo '{filename}' no existe en esta carpeta.", 404

if __name__ == '__main__':
    print("\n" + "="*50)
    print(" SERVIDOR DE PRUEBAS ACTIVO")
    print(" Dirección: http://127.0.0.1:5000")
    print("="*50 + "\n")
    app.run(debug=True, port=5000)
