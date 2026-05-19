import sys
import os

# Añadimos la carpeta actual al path para que Python encuentre app.py
sys.path.insert(0, os.path.dirname(__file__))

# Importamos la aplicación desde app.py
# Passenger espera que el objeto se llame 'application'
from app import app as application
