import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="******************",
    password="***************",
    database="tienda_muebles"
)

cursor = conexion.cursor(dictionary=True)

# Ejecutar consulta
cursor.execute("SELECT * FROM categoria")

# Obtener resultados
resultados = cursor.fetchall()

# Mostrar resultados
for fila in resultados:
    print(fila)

# Cerrar conexión
cursor.close()
conexion.close()
