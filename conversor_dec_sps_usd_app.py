# Importaciones.
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtGui import QDoubleValidator
from gui_sps_dec_usd_converter import *
from f_conversor_dec_sps_usd import *

# Clase personalizada para controlar excepciones en lineEdits cuando el valor de una entrada es negativo.
class NegativeValue_Exception(Exception):
    
    pass

# Clase App.
class Converter_app(QDialog):

    # Método Constructor.
    def __init__(self):

        # Llamado a constructor padre.
        super().__init__()

        # Se crea objeto de la clase que tiene la GUI.
        self.ui=Ui_converter_window()

        # Se cargan componentes de la GUI.
        self.ui.setupUi(self)

        # Se activa el botón de minimizar en la ventana (QDialog).
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowMinimizeButtonHint)

        # Se deshabilita la opción para redimensionar la ventana.
        self.setFixedSize(self.size())

        # Se crea validador decimal para sólo permitir escribir números decimales en los QLineEdits.
        validador_decimal=QDoubleValidator()

        # Se asigna validador decimal a los QLineEdits.
        self.ui.lineEdit_dec.setValidator(validador_decimal)
        self.ui.lineEdit_usd_dec.setValidator(validador_decimal)
        self.ui.lineEdit_sps.setValidator(validador_decimal)
        self.ui.lineEdit_usd_sps.setValidator(validador_decimal)
        
        # Se llama a función para obtener las tasas de conversión a USD del DEC y SPS.
        self.dict_prices=get_dec_sps_prices()
        #print(self.dict_prices)

        # Se asigna valores por defecto a QLineEdits.
        self.ui.lineEdit_dec.setText("1")
        self.ui.lineEdit_sps.setText("1")
        self.ui.lineEdit_usd_dec.setText(f'{self.dict_prices["dec_price"]:.5f}')
        self.ui.lineEdit_usd_sps.setText(f'{self.dict_prices["sps_price"]:.4f}')

        # Eventos.
        self.ui.lineEdit_dec.textChanged.connect(self.leer_entrada_dec)
        self.ui.lineEdit_usd_dec.textChanged.connect(self.leer_entrada_usd_dec)
        self.ui.lineEdit_sps.textChanged.connect(self.leer_entrada_sps)
        self.ui.lineEdit_usd_sps.textChanged.connect(self.leer_entrada_usd_sps)

        # Se muestra GUI.
        self.show()

    # Método para leer valor de lineEdit_dec.
    def leer_entrada_dec(self):

        # Bloque para manejar excepciones en la entrada de datos del lineEdit.
        try:

            # Se desactiva la señal para el evento en el lineEdit_usd_dec mientras se leen los valores del lineEdit_dec.
            # De esta forma se evita un error con un bucle infinito entre ambos eventos de los lineEdits.
            self.ui.lineEdit_usd_dec.blockSignals(True)

            # Se guarda valor de lineEdit_dec.
            dec_value=self.ui.lineEdit_dec.text()

            # Condicional para verificar si el dec_value tiene coma.
            if ',' in dec_value:

                # Se eliminan las comas del string.
                # Es necesario eliminar las comas para evitar un error de casting.
                dec_value=dec_value.replace(',','')

            # Condicional para verificar si la entrada es una cadena vacía.
            if dec_value == "":

                # Se ajusta valor a 0.
                dec_value=0

            # Condicional para verificar si la entrada es negativa.
            if float(dec_value)<0:

                # Se lanza excepción para controlar error.
                raise NegativeValue_Exception

            # Se calcula el equivalente de la cantidad ingresada en DEC a USD.
            usd_dec_value=float(dec_value)*self.dict_prices["dec_price"]

            # Condicional para verificar si usd_dec_value es inf.
            if str(usd_dec_value)=='inf':
                
                # Se ajustan valores de lineEdit_dec y lineEdit_usd_dec a sus valores iniciales.
                self.ui.lineEdit_dec.setText("1")
                usd_dec_value=self.dict_prices["dec_price"]

            # Se actualiza valor en lineEdit_usd_dec.
            self.ui.lineEdit_usd_dec.setText(f'{usd_dec_value:,.3f}')

            # Se habilita la señal para el evento en el lineEdit_usd_dec.
            self.ui.lineEdit_usd_dec.blockSignals(False)

        # Bloque para manejar excepciones en la entrada de datos del lineEdit.
        except ValueError:

            # Se crea un cuadro de diálogo de error.
            error_box = QMessageBox()

            # Se agrega el ícono de error.
            error_box.setIcon(QMessageBox.Critical)
            
            # Se agrega un título.
            error_box.setWindowTitle("Error")
            
            # Se agrega un mensaje en el interior de la ventana.
            error_box.setText("Debe introducir un número")

            # Se guarda la ruta absoluta a la imagen para usar como icono.
            ruta_icono=resource_path('spl-logo.png')

            # Se agrega un ícono a la ventana de error.
            error_box.setWindowIcon(QIcon(ruta_icono))
            
            # Se específica un botón "Ok" para la ventana.
            error_box.setStandardButtons(QMessageBox.Ok)

            # Se limpia lineEdit_dec.
            self.ui.lineEdit_dec.setText("")

            # Se muestra el cuadro de diálogo y espera hasta que el usuario lo cierre.
            error_box.exec_()

        # Bloque para manejar excepciones en la entrada de datos del lineEdit.
        except NegativeValue_Exception:

            # Se crea un cuadro de diálogo de error.
            error_box = QMessageBox()

            # Se agrega el ícono de error.
            error_box.setIcon(QMessageBox.Critical)
            
            # Se agrega un título.
            error_box.setWindowTitle("Error")
            
            # Se agrega un mensaje en el interior de la ventana.
            error_box.setText("Introduzca un número positivo")

            # Se guarda la ruta absoluta a la imagen para usar como icono.
            ruta_icono=resource_path('spl-logo.png')

            # Se agrega un ícono a la ventana de error.
            error_box.setWindowIcon(QIcon(ruta_icono))
            
            # Se específica un botón "Ok" para la ventana.
            error_box.setStandardButtons(QMessageBox.Ok)

            # Se limpia lineEdit_dec.
            self.ui.lineEdit_dec.setText("")

            # Se muestra el cuadro de diálogo y espera hasta que el usuario lo cierre.
            error_box.exec_()

    # Método para leer valor de lineEdit_usd_dec.
    def leer_entrada_usd_dec(self):

        # Bloque para manejar excepciones en la entrada de datos del lineEdit.
        try:
            # Se desactiva la señal para el evento en el lineEdit_dec mientras se leen los valores del lineEdit_usd_dec.
            # De esta forma se evita un error con un bucle infinito entre ambos eventos de los lineEdits.
            self.ui.lineEdit_dec.blockSignals(True)

            # Se guarda valor de lineEdit_usd_dec.
            usd_dec_value=self.ui.lineEdit_usd_dec.text()

            # Condicional para verificar si el usd_dec_value tiene coma.
            if ',' in usd_dec_value:

                # Se eliminan las comas del string.
                # Es necesario eliminar las comas para evitar un error de casting.
                usd_dec_value=usd_dec_value.replace(',','')

            # Condicional para verificar si la entrada es una cadena vacía.
            if usd_dec_value == "":

                # Se ajusta valor a 0.
                usd_dec_value=0

            # Condicional para verificar si la entrada es negativa.
            if float(usd_dec_value)<0:
             
                # Se lanza excepción para controlar error.
                raise NegativeValue_Exception
    
            # Se calcula el equivalente de la cantidad ingresada en USD a DEC.
            dec_value=float(usd_dec_value)/self.dict_prices["dec_price"]

            # Condicional para verificar si dec_value es inf.
            if str(dec_value)=='inf':
                
                # Se ajustan valores de lineEdit_dec y lineEdit_usd_dec a sus valores iniciales.
                dec_value=1
                self.ui.lineEdit_usd_dec.setText(f'{self.dict_prices["dec_price"]:.5f}')

            # Se actualiza valor en lineEdit_dec.
            self.ui.lineEdit_dec.setText(f'{dec_value:,.3f}')
            
            # Se habilita la señal para el evento en el lineEdit_dec.
            self.ui.lineEdit_dec.blockSignals(False)

        # Bloque para manejar excepciones en la entrada de datos del lineEdit.
        except ValueError:
            
            # Se crea un cuadro de diálogo de error.
            error_box = QMessageBox()

            # Se agrega el ícono de error.
            error_box.setIcon(QMessageBox.Critical)
            
            # Se agrega un título.
            error_box.setWindowTitle("Error")
            
            # Se agrega un mensaje en el interior de la ventana.
            error_box.setText("Debe introducir un número")

            # Se guarda la ruta absoluta a la imagen para usar como icono.
            ruta_icono=resource_path('spl-logo.png')

            # Se agrega un ícono a la ventana de error.
            error_box.setWindowIcon(QIcon(ruta_icono))
            
            # Se específica un botón "Ok" para la ventana.
            error_box.setStandardButtons(QMessageBox.Ok)
            
            # Se limpia lineEdit_usd_dec.
            self.ui.lineEdit_usd_dec.setText("")

            # Se muestra el cuadro de diálogo y espera hasta que el usuario lo cierre.
            error_box.exec_()
        
        # Bloque para manejar excepciones en la entrada de datos del lineEdit.
        except NegativeValue_Exception:

            # Se crea un cuadro de diálogo de error.
            error_box = QMessageBox()

            # Se agrega el ícono de error.
            error_box.setIcon(QMessageBox.Critical)
            
            # Se agrega un título.
            error_box.setWindowTitle("Error")
            
            # Se agrega un mensaje en el interior de la ventana.
            error_box.setText("Introduzca un número positivo")

            # Se guarda la ruta absoluta a la imagen para usar como icono.
            ruta_icono=resource_path('spl-logo.png')

            # Se agrega un ícono a la ventana de error.
            error_box.setWindowIcon(QIcon(ruta_icono))
            
            # Se específica un botón "Ok" para la ventana.
            error_box.setStandardButtons(QMessageBox.Ok)

            # Se limpia lineEdit_usd_dec.
            self.ui.lineEdit_usd_dec.setText("")

            # Se muestra el cuadro de diálogo y espera hasta que el usuario lo cierre.
            error_box.exec_()

    # Método para leer valor del lineEdit_sps.
    def leer_entrada_sps(self):

        # Bloque para manejar excepciones en la entrada de datos del lineEdit.
        try:
        
            # Se desactiva la señal para el evento en el lineEdit_usd_sps mientras se leen los valores del lineEdit_sps.
            # De esta forma se evita un error con un bucle infinito entre ambos eventos de los lineEdits.
            self.ui.lineEdit_usd_sps.blockSignals(True)

            # Se guarda valor de lineEdit_sps.
            sps_value=self.ui.lineEdit_sps.text()

            # Condicional para verificar si el sps_value tiene coma.
            if ',' in sps_value:

                # Se eliminan las comas del string.
                # Es necesario eliminar las comas para evitar un error de casting.
                sps_value=sps_value.replace(',','')

            # Condicional para verificar si la entrada es una cadena vacía.
            if sps_value == "":

                # Se ajusta valor a 0.
                sps_value=0
            
            # Condicional para verificar si la entrada es negativa.
            if float(sps_value)<0:

                # Se lanza excepción para controlar error.
                raise NegativeValue_Exception

            # Se calcula el equivalente de la cantidad ingresada en SPS a USD.
            usd_sps_value=float(sps_value)*self.dict_prices["sps_price"]

            # Condicional para verificar si usd_sps_value es inf.
            if str(usd_sps_value)=='inf':
                
                # Se ajustan valores de lineEdit_sps y lineEdit_usd_sps a sus valores iniciales.
                self.ui.lineEdit_sps.setText("1")
                usd_sps_value=self.dict_prices["sps_price"]

            # Se actualiza valor en lineEdit_usd_sps.
            self.ui.lineEdit_usd_sps.setText(f'{usd_sps_value:,.3f}')

            # Se habilita la señal para el evento en el lineEdit_usd_sps.
            self.ui.lineEdit_usd_sps.blockSignals(False)

        # Bloque para manejar excepciones en la entrada de datos del lineEdit.
        except ValueError:

            # Se crea un cuadro de diálogo de error.
            error_box = QMessageBox()

            # Se agrega el ícono de error.
            error_box.setIcon(QMessageBox.Critical)
            
            # Se agrega un título.
            error_box.setWindowTitle("Error")
            
            # Se agrega un mensaje en el interior de la ventana.
            error_box.setText("Debe introducir un número")

            # Se guarda la ruta absoluta a la imagen para usar como icono.
            ruta_icono=resource_path('spl-logo.png')

            # Se agrega un ícono a la ventana de error.
            error_box.setWindowIcon(QIcon(ruta_icono))
            
            # Se específica un botón "Ok" para la ventana.
            error_box.setStandardButtons(QMessageBox.Ok)

            # Se limpia lineEdit_sps.
            self.ui.lineEdit_sps.setText("")

            # Se muestra el cuadro de diálogo y espera hasta que el usuario lo cierre.
            error_box.exec_()

        # Bloque para manejar excepciones en la entrada de datos del lineEdit.
        except NegativeValue_Exception:

            # Se crea un cuadro de diálogo de error.
            error_box = QMessageBox()

            # Se agrega el ícono de error.
            error_box.setIcon(QMessageBox.Critical)
            
            # Se agrega un título.
            error_box.setWindowTitle("Error")
            
            # Se agrega un mensaje en el interior de la ventana.
            error_box.setText("Introduzca un número positivo")

            # Se guarda la ruta absoluta a la imagen para usar como icono.
            ruta_icono=resource_path('spl-logo.png')

            # Se agrega un ícono a la ventana de error.
            error_box.setWindowIcon(QIcon(ruta_icono))
            
            # Se específica un botón "Ok" para la ventana.
            error_box.setStandardButtons(QMessageBox.Ok)

            # Se limpia lineEdit_sps.
            self.ui.lineEdit_sps.setText("")

            # Se muestra el cuadro de diálogo y espera hasta que el usuario lo cierre.
            error_box.exec_()

    # Método para leer valor de lineEdit_usd_sps.
    def leer_entrada_usd_sps(self):

        # Bloque para manejar excepciones en la entrada de datos del lineEdit.
        try:

            # Se desactiva la señal para el evento en el lineEdit_sps mientras se leen los valores del lineEdit_usd_sps.
            # De esta forma se evita un error con un bucle infinito entre ambos eventos de los lineEdits.
            self.ui.lineEdit_sps.blockSignals(True)

            # Se guarda valor de lineEdit_usd_sps.
            usd_sps_value=self.ui.lineEdit_usd_sps.text()

            # Condicional para verificar si el usd_sps_value tiene coma.
            if ',' in usd_sps_value:

                # Se eliminan las comas del string.
                # Es necesario eliminar las comas para evitar un error de casting.
                usd_sps_value=usd_sps_value.replace(',','')

            # Condicional para verificar si la entrada es una cadena vacía.
            if usd_sps_value == "":

                # Se ajusta valor a 0.
                usd_sps_value=0
            
            # Condicional para verificar si la entrada es negativa.
            if float(usd_sps_value)<0:

                # Se lanza excepción para controlar error.
                raise NegativeValue_Exception

            # Se calcula el equivalente de la cantidad ingresada en USD a SPS.
            sps_value=float(usd_sps_value)/self.dict_prices["sps_price"]

            # Condicional para verificar si sps_value es inf.
            if str(sps_value)=='inf':
                
                # Se ajustan valores de lineEdit_sps y lineEdit_usd_sps a sus valores iniciales.
                sps_value=1
                self.ui.lineEdit_usd_sps.setText(f'{self.dict_prices["sps_price"]:.4f}')

            # Se actualiza valor en lineEdit_sps.
            self.ui.lineEdit_sps.setText(f'{sps_value:,.3f}')
            
            # Se habilita la señal para el evento en el lineEdit_sps.
            self.ui.lineEdit_sps.blockSignals(False)
        
        # Bloque para manejar excepciones en la entrada de datos del lineEdit.
        except ValueError:

            # Se crea un cuadro de diálogo de error.
            error_box = QMessageBox()

            # Se agrega el ícono de error.
            error_box.setIcon(QMessageBox.Critical)
            
            # Se agrega un título.
            error_box.setWindowTitle("Error")
            
            # Se agrega un mensaje en el interior de la ventana.
            error_box.setText("Debe introducir un número")

            # Se guarda la ruta absoluta a la imagen para usar como icono.
            ruta_icono=resource_path('spl-logo.png')

            # Se agrega un ícono a la ventana de error.
            error_box.setWindowIcon(QIcon(ruta_icono))
            
            # Se específica un botón "Ok" para la ventana.
            error_box.setStandardButtons(QMessageBox.Ok)

            # Se limpia lineEdit_usd_sps.
            self.ui.lineEdit_usd_sps.setText("")

            # Se muestra el cuadro de diálogo y espera hasta que el usuario lo cierre.
            error_box.exec_()

                # Bloque para manejar excepciones en la entrada de datos del lineEdit.
        except NegativeValue_Exception:

            # Se crea un cuadro de diálogo de error.
            error_box = QMessageBox()

            # Se agrega el ícono de error.
            error_box.setIcon(QMessageBox.Critical)
            
            # Se agrega un título.
            error_box.setWindowTitle("Error")
            
            # Se agrega un mensaje en el interior de la ventana.
            error_box.setText("Introduzca un número positivo")

            # Se guarda la ruta absoluta a la imagen para usar como icono.
            ruta_icono=resource_path('spl-logo.png')

            # Se agrega un ícono a la ventana de error.
            error_box.setWindowIcon(QIcon(ruta_icono))
            
            # Se específica un botón "Ok" para la ventana.
            error_box.setStandardButtons(QMessageBox.Ok)

            # Se limpia lineEdit_usd_sps.
            self.ui.lineEdit_usd_sps.setText("")

            # Se muestra el cuadro de diálogo y espera hasta que el usuario lo cierre.
            error_box.exec_()

# Condicional para iniciar aplicación.
if __name__=='__main__':

    # Creamos objeto para iniciar la aplicación.
    app=QApplication(sys.argv)

    # Creamos objeto de la clase Converter_app.
    ventana=Converter_app()
    
    # Para finalizar aplicación.
    sys.exit(app.exec_())





