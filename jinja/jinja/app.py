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
        
        return render_template("Productos.html")
    return render_template("Productos.html")
    
    
@app.route("/ver_carrito", methods = ["GET", "POST"])
def ver_carrito():
    if request.method == "POST":
        
        mueble_seleccionado = request.form.get("id_mueble")
        
        connexion, cursor = db_helper.get_base_datos
        
        sSQL = """select m.nombre, m.precio, dp.descripcion 
        from mueble m
        left join diseño_personalizado dp on m.id_mueble = dp.id_mueble
        where m.id_mueble = %s"""
        
        cursor.execute(sSQL, (mueble_seleccionado,))
        mueble = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        
        return render_template("Productos.html")
    return render_template("Productos.html")
        
        
        


@app.route("/hashear", methods = ["GET", "POST"])
def hashear():
    hash = generate_password_hash("1234")
    return hash
    
    
    # QUEDA PENDIENTE UNIFICAR TODAS LAS FUNCIONES DE FILTRADO EN LA RUTA /productos
    
    
@app.route("/productos", methods = ["GET", "POST"])
def pagina_productos():
    
    rol_usuario = session.get("rol", "cliente")
    
    accion = request.form.get("accion")
    
    productos = []
    mensaje = ""
    
    if request.method == "POST":
        
        p_min = request.form.get("p_min")
        p_max = request.form.get("p_max")
        color = request.form.get("color")
        material = request.form.get("material")
        seccion = request.form.get("secciones")
        
        if p_min or p_max:
            productos, mensaje = filtrar_por_precio()
            
        elif seccion:
            productos, mensaje = filtrar_por_seccion()
            
        elif color:
            productos, mensaje = filtro_por_color()
            
        elif material:
            productos, mensaje = filtro_por_material()
            
        else:
            conexion, cursor = db_helper.get_base_datos()
            
            sSQL = """select m.nombre, m.material, m.precio, dp.ancho,
                dp.alto, dp.profundidad, dp.color, dp.descripcion, dp.estado 
                from mueble m
                left join diseño_personalizado dp on m.id_mueble = dp.id_mueble
                """
                
            cursor.execute(sSQL)
            productos = cursor.fetchall()
            
            cursor.close()
            conexion.close()
            
        return render_template("Productos.html", productos = productos, mensaje = mensaje, rol_usuario = rol_usuario)
    else:
        
        conexion, cursor = db_helper.get_base_datos()
    
    
        sSQL = """select m.nombre, m.material, m.precio, dp.ancho,
            dp.alto, dp.profundidad, dp.color, dp.descripcion, dp.estado 
            from mueble m
            left join diseño_personalizado dp on m.id_mueble = dp.id_mueble 
                """
    
        cursor.execute(sSQL)
        productos = cursor.fetchall()
        
       
        cursor.close()
        conexion.close()
    
        # Obtener rol del usuario si está logueado (por defecto cliente)
        rol_usuario = session.get("rol", "cliente")
    
        return render_template("Productos.html", productos = productos, rol_usuario = rol_usuario, mensaje = mensaje)
        
 
 
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
    return muebles, ""
    
    

def filtrar_por_precio():
    
    precio_min = request.form.get("p_min") 
    precio_max = request.form.get("p_max")

    mensaje = ""
    muebles = []
        
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
        
        conexion, cursor = db_helper.get_base_datos()
        
        if not precio_min:
            cursor.execute("select min(precio) as minimo from mueble")
            resultado_min = cursor.fetchone()
            precio_min_numero = float(resultado_min["minimo"])
        else:
            precio_min_numero = float(precio_min)
            
        if not precio_max:
            cursor.execute("select max(precio) as maximo from mueble")
            resultado_max = cursor.fetchone()
            precio_max_numero = float(resultado_max["maximo"])
        else:
            precio_max_numero = float(precio_max)
            
        sSQL = """select m.nombre, m.material, m.precio, dp.ancho,
        dp.alto, dp.profundidad, dp.color, dp.descripcion, dp.estado 
        from mueble m
        left join diseño_personalizado dp on m.id_mueble = dp.id_mueble 
        where m.precio between %s and %s"""
        
        cursor.execute(sSQL,(precio_min_numero, precio_max_numero))
        muebles = cursor.fetchall()
            
        cursor.close()
        conexion.close()
            
    return muebles, mensaje
    
    
    
def filtrar_por_seccion():

    seccion_seleccionada = request.form.get("secciones")
    

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
    return muebles, ""
    
    
    
    
def filtro_por_color():

    color_seleccionado = request.form.get("color")

    conexion, cursor = db_helper.get_base_datos()

    sSQL = """select m.nombre, m.material, m.precio, dp.ancho,
        dp.alto, dp.profundidad, dp.color, dp.descripcion, dp.estado 
        from mueble m
        left join diseño_personalizado dp on m.id_mueble = dp.id_mueble
        where dp.color = %s
    """
    cursor.execute(sSQL, (color_seleccionado,))
    
    filtro_color = cursor.fetchall()

    cursor.close()
    conexion.close()
    
    return filtro_color, ""
    


def filtro_por_material():
    material_seleccionado = request.form.get("material")
    
    conexion, cursor = db_helper.get_base_datos()
    
    sSQL = """select m.nombre, m.material, m.precio, dp.ancho,
            dp.alto, dp.profundidad, dp.color, dp.descripcion, dp.estado 
            from mueble m
            left join diseño_personalizado dp on m.id_mueble = dp.id_mueble 
            where m.material = %s"""
    
    cursor.execute(sSQL, (material_seleccionado, ))
    
    filtro_material = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    
    return filtro_material, ""
    





@app.route("/logout", methods =["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)