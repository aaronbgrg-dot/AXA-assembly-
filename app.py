from flask import Flask, url_for, render_template, redirect, session, request
import mysql.connector
import db_helper
from werkzeug.security import generate_password_hash, check_password_hash
import os


load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("secret_key")

@app.route("/")
def home():
    return redirect(url_for("pagina_principal"))

@app.route("/Pagina_Principal")
def pagina_principal():
    return render_template("pagina_principal.html")

@app.route("/login", methods = ["GET","POST"])
def login():

    mensaje = ""

    if request.method == "POST":
        usuario_entrada = request.form.get("###")
        contrasena_entrada = request.form.get("###")

        conexion, cursor = db_helper.get_base_datos()

        sSQL = """select id_usuario, usuario, contrasena, rol 
        from usuario 
        where usuario = %s"""
        cursor.execute(sSQL, [usuario_entrada])
        usuario = cursor.fetchone()

        if check_password_hash(usuario["contrasena"], contrasena_entrada):
            session ["id_usuario"] = usuario ["id_usuario"]
            session ["usuario"] = usuario ["usuario"]
            return redirect(url_for("###"))
        else:
            mensaje = "Has introducido mal o el usuario o la contraseña!!"

        cursor.close()
        conexion.close()

    return render_template("login.html", mensaje=mensaje)

@app.route("/registrar_cliente", methods = ["GET","POST"])
def registrar_cliente():

    simbolos_contrasena = ["@", "¿", "¡", "_", "-"]
    mensaje = ""

    if request.method == "POST":
        usuario_entrada = request.form.get("###")
        contrasena_entrada = request.form.get("###")

        contrasena_segura = generate_password_hash(contrasena_entrada)

        conexion, cursor = db_helper.get_base_datos()

        contiene_numero = any(varchar.isdigit() for varchar in contrasena_entrada)
        contiene_simbolo = any(varchar in simbolos_contrasena for varchar in contrasena_entrada)


        if len(contrasena_entrada) < 8: 
            mensaje = "La contraseña debe tener al menos 8 caracteres."
            return render_template("###.html", mensaje = mensaje)
        elif not contiene_numero:
            mensaje = "La contraseña debe contener al menos 1 digito"
            return render_template("###.html", mensaje = mensaje)
        elif not contiene_simbolo:
            mensaje = "La contraseña debe contener uno de estos simbolos: @, ¿, ¡, _, -"
            return render_template("###.html", mensaje = mensaje) 

        else:
            sSQL = """insert into usuario (usuario, contrasena, rol) 
            values(%s,%s,%s)"""            
            cursor.execute(sSQL,(usuario_entrada, contrasena_segura, "cliente"))

        cursor.close()
        conexion.close()

        return redirect(url_for("###"))
    return render_template("###.html")


@app.route("/ordenar_por_precio", methods = ["GET", "POST"])
def ordenar_por_precio():
    
    conexion, cursor = db_helper.get_base_datos()

    sSQL = """select m.nombre, m.material, m.precio, dp.ancho,
    dp.alto, dp.profundidad, dp.color, dp.descripcion, dp.estado 
    from mueble m 
    left join diseño_personalizado dp on m.id_mueble = dp.id_mueble 
    order by m.precio asc"""

    cursor.execute(sSQL)

    muebles = cursor.fetchall()

    cursor.close()
    conexion.close()
    return render_template("###.html", muebles = muebles)


@app.route("/filtrar_por_precio", methods = ["GET", "POST"])
def filtrar_por_precio():
    if request.method == "POST":
        precio_min = request.form.get("Valor min introducido por el usuario") 
        precio_max = request.form.get("valor max introducido por usuario")

        conexion, cursor = db_helper.get_base_datos()

        sSQL = """select m.nombre, m.material, m.precio, dp.ancho,
        dp.alto, dp.profundidad, dp.color, dp.descripcion, dp.estado 
        from mueble m
        left join diseño_personalizado dp on m.id_mueble = dp.id_mueble 
        where m.precio between %s and %s"""
        cursor.execute(sSQL, (precio_min, precio_max))

        muebles = cursor.fetchall()

        cursor.close()
        conexion.close()
        return render_template("###.html", muebles = muebles)
    return render_template("###.html")

@app.route("/filtrar_por_seccion", methods = ["GET", "POST"])
def filtrar_por_seccion():

    if request.method == "POST":
        seccion_seleccionada = request.form.get("seccion")
        

        conexion, cursor = db_helper.get_base_datos()

        sSQL = """select m.nombre, m.material, m.precio, dp.ancho,
        dp.alto, dp.profundidad, dp.color, dp.descripcion, dp.estado 
        from mueble m
        left join diseño_personalizado dp on m.id_mueble = dp.id_mueble
        where m.categoria = %s"""
        cursor.execute(sSQL, [seccion_seleccionada])

        muebles = cursor.fetchall()
    
        cursor.close()
        conexion.close()
        return render_template("###.html", muebles = muebles)
    return render_template("###.html")


@app.route("/añadir_muebles", methods = ["GET", "POST"])
def añadir_muebles():

    mensaje = ""

    if request.method == "POST":
        nombre_mueble_nuevo = request.form.get("nombre_nuevo")
        precio_mueble_nuevo = request.form.get("precio_nuevo")
        categoria_mueble_nuevo = request.form.get("categoria_nueva")
        cantidad_mueble_nuevo = request.form.get("stock")
        material_mueble_nuevo = request.form.get("material_mueble_nuevo")
        descripción_mueble_nuevo = request.form.get("imagen_nueva")
        altura_mueble_nuevo = request.form.get("altura_nuevo")
        anchura_mueble_nuevo = request.form.get("anchura_nueva")
        profundidad_mueble_nuevo = request.form.get("profundidad_nueva")

        conexion, cursor = db_helper.get_base_datos()

        sSQL = """insert into mueble (nombre, categoria, precio, stock, material) 
        values(%s, %s, %s, %s, %s) """
        cursor.execute(sSQL, (nombre_mueble_nuevo, categoria_mueble_nuevo, precio_mueble_nuevo, cantidad_mueble_nuevo, material_mueble_nuevo))

        sSQL = """ insert into diseño_personalizado(ancho, alto, profundidad, color, material, descripcion, precio_estimado, estado) values(%s, %s, %s, %s, %s, %s, %s, %s)
"""

        cursor.close()
        conexion.close()

        mensaje = "Muebles añadidos con exito."
        return render_template ("###.html", mensaje = mensaje)
    return render_template("###.html")




@app.route("/logout", methods =["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)