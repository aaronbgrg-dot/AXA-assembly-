from flask import Flask, url_for, render_template, redirect, session, request
import mysql.connector
import db_helper
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
import re


app = Flask(__name__)

app.secret_key = os.getenv("secret_key")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    mensaje = ""
    if request.method == "POST":
        
        usuario_entrada = request.form.get("Nom_usuario")
        contrasena_entrada = request.form.get("Contrase_usuario")
        
        conexion, cursor = db_helper.get_base_datos()
        
        sSQL = """select id_usuario, nombre, contrasena, rol 
        from usuario 
        where nombre = %s"""
        
        cursor.execute(sSQL, (usuario_entrada,))
        
        usuario = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        
        if usuario and check_password_hash(usuario["contrasena"], contrasena_entrada):
            session["id_usuario"] = usuario["id_usuario"]
            session["usuario"] = usuario["nombre"]
            
            return redirect(url_for("home"))
            
        else:
            mensaje = "Has introducido mal o el usuario o la contrasena!!"
            
    return render_template("Login.html", mensaje=mensaje)
    
    

@app.route("/registro", methods = ["GET","POST"])
def registro():

    simbolos_contrasena = ["@", "¿", "¡", "_", "-"]
    mensaje = ""

    if request.method == "POST":
        usuario_entrada = request.form.get("Nom_cliente")
        apellido_entrada = request.form.get("apellido_cliente")
        email_entrada = request.form.get("email_cliente")
        contrasena_entrada = request.form.get("Contrase_cliente")
        telefono_entrada = request.form.get("telefono_cliente")
        

        conexion, cursor = db_helper.get_base_datos()

        contiene_numero = any(varchar.isdigit() for varchar in contrasena_entrada)
        contiene_simbolo = any(varchar in simbolos_contrasena for varchar in contrasena_entrada)

        
        if len(contrasena_entrada) < 8: 
            mensaje = "La contraseña debe tener al menos 8 caracteres."
            return render_template("Registro.html", mensaje = mensaje)
        elif not contiene_numero:
            mensaje = "La contraseña debe contener al menos 1 digito"
            return render_template("Registro.html", mensaje = mensaje)
        elif not contiene_simbolo:
            mensaje = "La contraseña debe contener uno de estos simbolos: @, ¿, ¡, _, -"
            return render_template("Registro.html", mensaje = mensaje)
            
            
        elif not comprobar_email(email_entrada):
            if not comprobar_telefono(telefono_entrada):
                mensaje = "El correo no es correcto y el numero de telefono debe tener 9 digitos"
            return render_template("Registro.html", mensaje = mensaje)
            
            
        elif not comprobar_telefono(telefono_entrada):
            mensaje = "El numero de telefono debe tener 9 digitos"
            return render_template("Registro.html", mensaje = mensaje)
            
        else:
            contrasena_segura = generate_password_hash(contrasena_entrada)
            
            sSQL = """insert into usuario (nombre, apellido, email, contrasena, telefono, rol, fecha_registro) 
            values(%s, %s, %s, %s, %s, %s, curdate())"""            
            cursor.execute(sSQL, (usuario_entrada, apellido_entrada, email_entrada, contrasena_segura, telefono_entrada, "cliente"))
            
            id_usuario_registrado = cursor.lastrowid
            
            session["id_usuario"] = id_usuario_registrado
            session["usuario"] = usuario_entrada
            
            cursor.close()
            conexion.close()
            
            return redirect(url_for("home"))
    return render_template("Registro.html", mensaje = mensaje)
    


def comprobar_telefono(telefono_cliente):
    
    if telefono_cliente and len(telefono_cliente) == 9 and telefono_cliente.isdigit():
        return True
    else:
        return False
    

def comprobar_email(email_cliente):
    # Esta expresión regular comprueba: texto + @ + texto + . + extensión
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(patron, email_cliente):
        return True
    return False
    
        


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
    mensaje = ""
    muebles = []
    if request.method == "POST":
        
        precio_min = request.form.get("Valor min introducido por el usuario") 
        precio_max = request.form.get("valor max introducido por usuario")

        if precio_min and precio_max:
            if precio_min.isdigit() and precio_max.isdigit():

                precio_min_numero = float(precio_min)
                precio_max_numero = float(precio_max)

                conexion, cursor = db_helper.get_base_datos()

                sSQL = """select m.nombre, m.material, m.precio, dp.ancho,
                dp.alto, dp.profundidad, dp.color, dp.descripcion, dp.estado 
                from mueble m
                left join diseño_personalizado dp on m.id_mueble = dp.id_mueble 
                where m.precio between %s and %s"""
                cursor.execute(sSQL,(precio_min_numero, precio_max_numero))

                muebles = cursor.fetchall()

                cursor.close()
                conexion.close()

                if not muebles:
                    mensaje = "No hay muebles en el rango escogido" 
            else:
                mensaje = "Introduce numeros por favor"

        else:
            mensaje = "Necesito que digas entre que precios quieres filtrar"
            
    return render_template("###.html", muebles = muebles, mensaje = mensaje)

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
        cursor.execute(sSQL, (seccion_seleccionada,))

        muebles = cursor.fetchall()
    
        cursor.close()
        conexion.close()
        return render_template("###.html", muebles = muebles)
    return render_template("index.html")


@app.route("/personalizar_muebles", methods = ["GET", "POST"])
def personalizar_muebles():

    mensaje = ""

    if request.method == "POST":
        tipo_mueble = request.form.get("tipo_mueble")          
        seccion_hogar = request.form.get("seccion_hogar")      
        color_mueble = request.form.get("color")
        anchura_mueble = request.form.get("ancho")
        altura_mueble = request.form.get("alto")
        profundidad_mueble = request.form.get("profundidad")
        material_mueble = request.form.get("material")
        descripcion_mueble = request.form.get("descripcion_mueble")
        precio_estimado_mueble = request.form.get("precio_estimado")
        estado_mueble = request.form.get("estado")

        conexion, cursor = db_helper.get_base_datos()

        sSQL = """select id_mueble
        from mueble 
        WHERE nombre = %s AND categoria = %s AND material = %s"""
        
        cursor.execute(sSQL, (tipo_mueble, seccion_hogar, material_mueble))
        id_mueble = cursor.fetchone()
        
        if id_mueble is None:
            mensaje = "Error: El mueble base seleccionado no existe en nuestro catalogo."
        
        else:
           
            id_mueble_catalogo = id_mueble["id_mueble"]
            id_usuario_sesion = session.get("id_usuario")
    
            sSQL = """ insert into diseño_personalizado(id_usuario, id_mueble, ancho, alto, profundidad, color, material, descripcion, precio_estimado, estado)
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sSQL, (id_usuario_sesion, id_mueble_catalogo, anchura_mueble, altura_mueble, profundidad_mueble, color_mueble, material_mueble, descripcion_mueble, precio_estimado_mueble, estado_mueble))
            
            mensaje = "Solicitud enviada con exito."
    
        cursor.close()
        conexion.close()
    
        
        return render_template ("Form_crear_mueble.html", mensaje = mensaje)
    return render_template("Form_crear_mueble.html")


@app.route("/filtro_por_color", methods = ["GET", "POST"])
def filtro_por_color():
    if request.method == "POST":
        color_seleccionado = request.form.get("color")

        conexion, cursor = db_helper.get_base_datos()

        sSQL = """select m.nombre, m.material, m.precio, dp.ancho,
            dp.alto, dp.profundidad, dp.color, dp.descripcion, dp.estado 
            from mueble m
            left join diseño_personalizado dp on m.id_mueble = dp.id_mueble
            where dp.color = %s
        """
        cursor.execute(sSQL, (color_seleccionado,))

        cursor.close()
        conexion.close()

        return render_template("###.html")
    return render_template("###.html")


@app.route("/get_feedback", methods = ["GET", "POST"])
def get_feedback():
    if request.method == "POST":

        id_usuario_sesion = session.get("id_usuario")
        nuevo_feedback = request.form.get("Feedback")
        # nueva_resena = request.form.get("resena")      solo si hace falta en la nueva base de datos

        conexion, cursor = db_helper.get_base_datos()

        sSQL = """insert into diseño_personalizado(id_usuario, id_mueble, ancho, alto, profundidad, color, material, descripcion, precio_estimado, estado) 
        values(%s, 1, 2000, 1400, 1100, "naranja", "algodon", %s, 1299, "montado")
        """
        id_pedido_valorador = cursor.lastrowid

        cursor.execute(sSQL, (id_usuario_sesion, nuevo_feedback))

        cursor.close()
        conexion.close()

        return render_template("index.html")
    return render_template("index.html")
    
    
@app.route("/anadir_al_carrito", methods = ["GET", "POST"])
def anadir_al_carrito():
    if request.method == "POST":
        
        id_usuario_actual = session.get("id_usuario")
        mueble_anadido = request.form.get("nombre_mueble")
        
        conexion, cursor = db_helper.get_base_datos()
        
        sSQL = """insert into carrito(id_usuario, mueble, cantidad) values(%s, %s, 1) """
        
        cursor.execute(sSQL,(id_usuario_actual, mueble_anadido))
        
        cursor.close()
        conexion.close()
        
        return redirect(url_for("###"))
    return render_template("###.html")
    
    
# @app.route("/ver_carrito", methods = ["GET", "POST"])
# def ver_carrito():
#     if request.method == "POST":
        

@app.route("/hashear", methods = ["GET", "POST"])
def hashear():
    hash = generate_password_hash("1234")
    return hash
    
@app.route("/productos", methods = ["GET", "POST"])
def pagina_productos():
    return render_template("Productos.html")


@app.route("/logout", methods =["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)