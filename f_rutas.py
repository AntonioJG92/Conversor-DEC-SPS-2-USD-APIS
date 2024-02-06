# Importaciones.
import sys
import os

# Función para determinar la ruta de una imagen dependiendo del entorno de ejecución.
# Bien sea un "entorno congelado" o un "entorno de desarrollo".
def resource_path(relative_path):
    
    # Se verifica si es el "entorno congelado (ejecutable)".
    if getattr(sys, 'frozen', False):
        
        # Estamos en un entorno congelado (PyInstaller).
        # Se guarda la ruta base.
        base_path = sys._MEIPASS
    
    # Entorno de desarrollo.
    else:
       
        # Estamos en un entorno normal de Python (Desarrollo).
        # Se guarda la ruta base.
        base_path = os.path.abspath(".")

    # Se retorna la ruta absoluta de acuerdo al entorno de ejecución.
    return os.path.join(base_path, relative_path)
