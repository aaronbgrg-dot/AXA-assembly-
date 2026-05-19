import sys
import os

# Forzamos la ruta de tu carpeta de muebles
cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, cwd)
os.chdir(cwd)

# Cargamos tu aplicacion Flask limpia
from app import app as application