# Importaciones
import requests
import sys
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
from f_rutas import *

# Función para obtener las tasas de conversión a USD del DEC y SPS.
def get_dec_sps_prices():

    # Bloque para manejar excepciones en petición GET.
    try:

        # Petición GET.
        response_get=requests.get('https://api.splinterlands.com/settings')

        # Objeto json con la respuesta de la petición.
        result_obj=response_get.json()

        # Diccionario con los los precios del DEC y SPS.
        # Se usa un diccionario de comprensión.
        dict_prices={token_key:result_obj[token_key] for token_key in ("dec_price", "sps_price")}

        # Se retorna diccionario con las tasas de conversión a USD para el DEC y SPS.
        return dict_prices

    # Bloque para manejar excepciones en petición GET.
    except:

        # Se crea un cuadro de diálogo de error.
        error_box = QMessageBox()

        # Se agrega el ícono de error.
        error_box.setIcon(QMessageBox.Critical)
        
        # Se agrega un título.
        error_box.setWindowTitle("Error")
        
        # Se agrega un mensaje en el interior de la ventana.
        error_box.setText("Error de conexión")

        # Se guarda la ruta absoluta a la imagen para usar como icono.
        ruta_icono=resource_path('spl-logo.png')

        # Se agrega un ícono a la ventana de error.
        error_box.setWindowIcon(QIcon(ruta_icono))
        
        # Se específica un botón "Ok" para la ventana.
        error_box.setStandardButtons(QMessageBox.Ok)

        # Se conecta el botón "Ok" a la función sys.exit.    
        error_box.buttonClicked.connect(sys.exit)

        # Se muestra el cuadro de diálogo y espera hasta que el usuario lo cierre.
        error_box.exec_()