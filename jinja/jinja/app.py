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
        where username = %s"""
        
        cursor.execute(sSQL, (usuario_entrada,))
        
        usuario = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        
        if usuario and check_password_hash(usuario["contrasena"], contrasena_entrada):
            session["id_usuario"] = usuario["id_usuario"]
            session["usuario"] = usuario["nombre"]
            session["rol"] = usuario["rol"]
            
            
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
        nombre_usuario_entrada = request.form.get("username")
        email_entrada = request.form.get("email_cliente")
        telefono_entrada = request.form.get("telefono_cliente")
        genero_entrada = request.form.get("genero")
        direccion_entrada = request.form.get("direccion_hogar")
        contrasena_entrada = request.form.get("Contrase_cliente")
        

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
            mensaje = "Por favor, introduce un correo electronico valido."
            return render_template("Registro.html", mensaje = mensaje)
            
        elif not comprobar_telefono(telefono_entrada):
            mensaje = "El numero de telefono debe tener 9 digitos"
            return render_template("Registro.html", mensaje = mensaje)
            
        else:
            
            rol_actual = session.get("rol")
            if rol_actual in ["empleado", "admin"]:
                departamento_empleado = session.get("id_departamento")
            else:
                departamento_empleado = None
            
            contrasena_segura = generate_password_hash(contrasena_entrada)
            
            sSQL = """insert into usuario (nombre, apellido, username, email, telefono, contrasena, genero, direccion_hogar,  rol, fecha_registro, id_departamento) 
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s, curdate(), %s)"""            
            cursor.execute(sSQL, (usuario_entrada, apellido_entrada, nombre_usuario_entrada, email_entrada, telefono_entrada, contrasena_segura, genero_entrada, direccion_entrada, "cliente", departamento_empleado))
            
            id_usuario_registrado = cursor.lastrowid
            
            session["id_usuario"] = id_usuario_registrado
            session["usuario"] = usuario_entrada
            session["rol"] = "cliente"
            session["id_departamento"] = departamento_empleado
            
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
    
    if "id_usuario" not in session:
        return redirect(url_for("login"))

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
        
        sSQL = """SELECT id_categoria 
        FROM categoria 
        WHERE nombre = %s"""
        cursor.execute(sSQL, (seccion_hogar,))
        resultado_categoria = cursor.fetchone()

        if resultado_categoria is None:
            mensaje = "Error: La sección del hogar no existe."
        else:
            id_categoria = resultado_categoria["id_categoria"]
    
            sSQL = """ insert into mueble(nombre, ancho, alto, profundidad, descripcion, precio, url_imagen, tipo_material, color, stock, id_categoria, id_proveedor)
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sSQL, (tipo_mueble, anchura_mueble, altura_mueble, profundidad_mueble, descripcion_mueble, precio_estimado_mueble,  "", material_mueble, color_mueble, -1, id_categoria, None))
            
            mensaje = "Solicitud enviada con exito."
        
        cursor.close()
        conexion.close()
    
        
        return render_template ("Form_crear_mueble.html", mensaje = mensaje)
    return render_template("Form_crear_mueble.html")
    

@app.route("/ver_pedidos", methods = ["GET", "POST"])
def ver_pedidos():
    
    if "id_usuario" not in session:
        return redirect(url_for("login"))
        
    sesion_usuario = session.get("id_usuario")
        
    conexion, cursor = db_helper.get_base_datos()
    
    sSQL="""select p.id_pedido, p.fecha_pedido, p.total, p.estado, m.id_mueble, m.nombre, m.url_imagen
    from pedido p
    left join mueble m on p.id_mueble = m.id_mueble
    where p.id_usuario = %s"""
    
    cursor.execute(sSQL, (sesion_usuario,))
    pedidos_muebles_usuario = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    
    return render_template("Pedidos.html", pedidos_muebles_usuario = pedidos_muebles_usuario)
    



@app.route("/get_feedback", methods = ["GET", "POST"])
def get_feedback():
    
    if "id_usuario" not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":

        id_usuario_sesion = session.get("id_usuario")
        nuevo_feedback = request.form.get("Feedback")
        estrellas_mueble = request.form.get("estrellas")
        id_mueble_feedback = request.form.get("id_mueble")
        
        
        if nuevo_feedback and estrellas_mueble and id_mueble_feedback:
            
            conexion, cursor = db_helper.get_base_datos()
    
            sSQL = """insert into feedback(id_usuario, id_mueble, estrellas, comentario, fecha_feedback) 
            values(%s, %s, %s, %s, curdate())
            """
            
            cursor.execute(sSQL, (id_usuario_sesion, id_mueble_feedback, estrellas_mueble, nuevo_feedback))
            
            cursor.close()
            conexion.close()

        return redirect(url_for("ver_pedidos"))
    return redirect(url_for("ver_pedidos"))
    
    
# @app.route("/anadir_al_carrito", methods = ["GET", "POST"])
# def anadir_al_carrito():
    
#     if "id_usuario" not in session:
#         return redirect(url_for("login"))
    
#     if request.method == "POST":
        
#         id_usuario_actual = session.get("id_usuario")
#         mueble_anadido = request.form.get("nombre_mueble")
        
#         conexion, cursor = db_helper.get_base_datos()
        
#         sSQL = """select id_mueble, precio 
#         from mueble
#         where nombre = %s"""
        
#         cursor.execute(sSQL, (mueble_anadido,))
#         mueble_seleccionado = cursor.fetchone()
        
#         id_mueble = mueble_seleccionado["id_mueble"]
#         precio_unitario = mueble_seleccionado["precio"]
        
#         sSQL = """select id_carrito 
#         from carrito 
#         where id_usuario = %s and estado = 'activo'"""
        
#         cursor.execute(sSQL,(id_usuario_actual, ))
#         carrito_actual = cursor.fetchone()
        
#         if carrito_actual:
#             id_carrito_actual = carrito_actual["id_carrito"]
            
#         else:
#             sSQL = """insert into carrito(id_usuario, fecha_creacion, estado)
#             values(%s, curdate(), 'activo')"""
#             cursor.execute(sSQL, (id_usuario_actual,))
            
#             id_carrito_actual = cursor.lastrowid
            
        
#         sSQL = """select cantidad 
#         from detalle_carrito
#         where id_mueble = %s and id_carrito = %s"""
        
#         cursor.execute(sSQL, (id_mueble, id_carrito_actual))
#         cantidad_existente = cursor.fetchone()
        
#         if cantidad_existente:
#             cantidad_final = cantidad_existente["cantidad"] + 1
            
#             sSQL = """update detalle_carrito 
#             set cantidad = %s 
#             where id_carrito = %s and id_mueble = %s"""
#             cursor.execute(sSQL, (cantidad_final, id_carrito_actual, id_mueble))
        
#         else:
            
#             sSQL = """insert into detalle_carrito(id_carrito, id_mueble, cantidad, precio_unitario) values(%s, %s, 1, %s)"""
            
#             cursor.execute(sSQL, (id_carrito_actual, id_mueble, precio_unitario))
        
        
#         cursor.close()
#         conexion.close()
        
#         return redirect(url_for("pagina_productos"))
#     return redirect(url_for("pagina_productos"))


# -----------------------------------------------------------------------
    
    
# @app.route("/ver_carrito", methods = ["GET", "POST"])
# def ver_carrito():
    
#     if "id_usuario" not in session:
#         return redirect(url_for("login"))
    
#     if request.method == "POST":
        
#         mueble_seleccionado = request.form.get("id_mueble")
        
#         conexion, cursor = db_helper.get_base_datos()
        
#         sSQL = """select nombre, precio, url_imagen 
#         from mueble 
#         where id_mueble = %s"""
        
#         cursor.execute(sSQL, (mueble_seleccionado,))
#         mueble = cursor.fetchone()
        
#         cursor.close()
#         conexion.close()
        
#         return render_template("Productos.html")
#     return redirect(url_for("pagina_productos"))
        
        
        


@app.route("/hashear", methods = ["GET", "POST"])
def hashear():
    hash = generate_password_hash("1234")
    return hash
    
  
    
    
@app.route("/productos", methods = ["GET", "POST"])
def pagina_productos():
    
    rol_usuario = session.get("rol", "cliente")
    
    accion = request.form.get("accion")
    
    productos = []
    mensaje = ""
    
    porcentaje = ofertas()
    
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
            
            sSQL = """select id_mueble, nombre, ancho, alto, profundidad, descripcion, precio, url_imagen, tipo_material, color, stock, id_categoria, id_proveedor
                from mueble 
                """
                
            cursor.execute(sSQL)
            productos = cursor.fetchall()
            
            cursor.close()
            conexion.close()
            
        
    else:
        
        conexion, cursor = db_helper.get_base_datos()
    
    
        sSQL = """select id_mueble, nombre, ancho, alto, profundidad, descripcion, precio, url_imagen, tipo_material, color, stock, id_categoria, id_proveedor
            from mueble 
            """
    
        cursor.execute(sSQL)
        productos = cursor.fetchall()
        
        cursor.close()
        conexion.close()
        
    for producto in productos:
        precio_original = float(producto["precio"])
        producto["precio_con_descuento"] = round(precio_original * (1 - (porcentaje / 100)), 2)
    
    
    # Obtener rol del usuario si está logueado (por defecto cliente)
    rol_usuario = session.get("rol", "cliente")

    return render_template("Productos.html", productos = productos, rol_usuario = rol_usuario, mensaje = mensaje, porcentaje = porcentaje)
        


def ofertas():
    
    conexion, cursor = db_helper.get_base_datos()
    
    sSQL = """select descuento
    from oferta
    where dia_especial = curdate()"""
    
    cursor.execute(sSQL)
    oferta_del_dia = cursor.fetchone()
    
    if oferta_del_dia:
    
        porcentaje = float(oferta_del_dia["descuento"])
        
    else:
        porcentaje = 0
        
        
    cursor.close()
    conexion.close()
    
    return porcentaje
    
        
        
 
 
def ordenar_por_precio():
    
    conexion, cursor = db_helper.get_base_datos()

    sSQL = """select *
    from mueble 
    order by precio asc"""

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

            sSQL = """select *
            from mueble 
            where precio between %s and %s"""
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
            
        sSQL = """select * 
            from mueble 
            where precio between %s and %s"""
        
        cursor.execute(sSQL,(precio_min_numero, precio_max_numero))
        muebles = cursor.fetchall()
            
        cursor.close()
        conexion.close()
            
    return muebles, mensaje
    
    
    
def filtrar_por_seccion():

    seccion_seleccionada = request.form.get("secciones")
    

    conexion, cursor = db_helper.get_base_datos()

    sSQL = """select * 
            from mueble m
            join categoria c on m.id_categoria = c.id_categoria
            where c.nombre = %s"""
    cursor.execute(sSQL, (seccion_seleccionada,))

    muebles = cursor.fetchall()

    cursor.close()
    conexion.close()
    return muebles, ""
    
    
    
    
def filtro_por_color():

    color_seleccionado = request.form.get("color")

    conexion, cursor = db_helper.get_base_datos()

    sSQL = """select *
        from mueble 
        
        where color = %s
    """
    cursor.execute(sSQL, (color_seleccionado,))
    
    filtro_color = cursor.fetchall()

    cursor.close()
    conexion.close()
    
    return filtro_color, ""
    


def filtro_por_material():
    material_seleccionado = request.form.get("material")
    
    conexion, cursor = db_helper.get_base_datos()
    
    sSQL = """select *
            from mueble 
            where tipo_material = %s"""
    
    cursor.execute(sSQL, (material_seleccionado, ))
    
    filtro_material = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    
    return filtro_material, ""
    
    
    

@app.route("/editar_mueble", methods=["GET","POST"])
def editar_mueble():
    
    if "id_usuario" not in session or session.get("rol") != "administrador":
        return redirect(url_for("pagina_productos"))

    if request.method == "POST":
        
        id_mueble_a_cambiar = request.form.get("id_mueble")
        nuevo_nombre = request.form.get("nombre")
        nuevo_precio = request.form.get("precio")
        nueva_imagen = request.form.get("url_imagen")
        nuevo_material = request.form.get("tipo_material")
        nuevo_color = request.form.get("color")
        nuevo_stock = request.form.get("stock")
        nuevo_ancho = request.form.get("ancho")
        nuevo_alto = request.form.get("alto")
        nueva_profundidad = request.form.get("profundidad")
        nueva_descripcion = request.form.get("descripcion")

        conexion, cursor = db_helper.get_base_datos()

        sSQL = """
            UPDATE mueble 
            SET nombre = %s, ancho = %s, alto = %s, profundidad = %s, descripcion = %s, precio = %s, url_imagen = %s, tipo_material = %s, color = %s, stock = %s
            WHERE id_mueble = %s
        """
        
        cursor.execute(sSQL, (nuevo_nombre, float(nuevo_ancho) if nuevo_ancho else None,float(nuevo_alto) if nuevo_alto else None,float(nueva_profundidad) if nueva_profundidad else None, nueva_descripcion, float(nuevo_precio), nueva_imagen,  nuevo_material, nuevo_color, int(nuevo_stock), id_mueble_a_cambiar))
        
        cursor.close()
        conexion.close()

    return redirect(url_for("pagina_productos"))
    
    
    
        





@app.route("/logout", methods =["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)