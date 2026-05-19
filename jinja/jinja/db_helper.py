import mysql.connector
from flask import session
import os
from dotenv import load_dotenv

# Cargamos el archivo .env
load_dotenv()

def get_base_datos():

    conexion = mysql.connector.connect(
        host = os.getenv("HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        database = os.getenv("DATABASE")
    )
    
    conexion.autocommit = True

    cursor = conexion.cursor(dictionary=True)
    cursor._conexion_padre = conexion
    return conexion, cursor
