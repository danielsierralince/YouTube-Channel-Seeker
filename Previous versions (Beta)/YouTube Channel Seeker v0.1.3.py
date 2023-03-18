#Librerías generales
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QPushButton, QDialog, QTableWidget, QVBoxLayout, QMessageBox, QTableWidgetItem, QInputDialog

#La clase de la ventana principal que posteriormente usaremos para instanciar el objeto
class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        #Atributos principales
        self.setWindowTitle('YouTube Channel Seeker')
        self.setGeometry(100, 100, 1000, 450)
        self.move(50, 100)
        self.centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralWidget)
        
        #La tabla
        self.tableWidget = QtWidgets.QTableWidget(self.centralWidget)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setColumnWidth(0,200)
        self.tableWidget.setColumnWidth(1,498)
        self.tableWidget.setColumnWidth(2,200)
        self.tableWidget.setHorizontalHeaderLabels(['Channel', 'Link', 'Category'])
        self.tableWidget.setGeometry(QtCore.QRect(50, 70, 900, 350))
        
        #FortiLogo
        pixmap = QtGui.QPixmap('img/fortilogo.png')
        icon = QtGui.QIcon(pixmap)
        self.setWindowIcon(icon)
        #self.setWindowIcon(QtGui.QIcon('img/fortilogo.png'))

        #El botón de añadir
        self.addRowButton = QPushButton('Add row', self.centralWidget)
        self.addRowButton.setGeometry(QtCore.QRect(50, 20, 100, 30))
        self.addRowButton.clicked.connect(self.mostrar_window2)
        
        #Mostrar la 2nda ventana        
    def mostrar_window2(self):
        self.secondary_window = Window2()
        self.secondary_window.exec_()
        
#Clase de la segunda ventana        
class Window2(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add row')
        self.setGeometry(100, 100, 400, 300)
        self.move(800, 201)
        
        #Creamos una tabla con dos columnas y tres filas
        self.table = QTableWidget()
        self.table.setColumnCount(1)
        self.table.setRowCount(3)
        self.table.setFixedSize(200, 200)
        
        #Añadimos algunos datos a la tabla
        self.table.setVerticalHeaderLabels(['Channel', 'Link', 'Category'])
        self.table.setHorizontalHeaderLabels(['1'])
        
        #Creamos un layout y añadimos la tabla a él
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
        
        #El boton de guardar
        self.addRowButton = QPushButton('Save', self)
        self.addRowButton.setGeometry(QtCore.QRect(260, 85, 100, 30))
        self.addRowButton.clicked.connect(self.save_data)
        
        #El boton de añadir
        self.addRowButton = QPushButton('Add', self)
        self.addRowButton.setGeometry(QtCore.QRect(260, 125, 100, 30))
        self.addRowButton.clicked.connect(self.add_data)
    
    #Funcion de guardado del boton Save    
    def save_data(self):
        #Recorremos la tabla y obtenemos los datos de cada celda
        data = []
        for fila in range(self.table.rowCount()):
            for columna in range(self.table.columnCount()):
                datos = self.table.item(fila, columna)
                if datos is not None:
                    data.append(datos.text())
        #####################################################
        # Guardamos los datos en un archivo o base de datos #
        #####################################################
        
        #En este caso, simplemente mostramos un mensaje
        QMessageBox.information(self, 'Save data', 'The data has been saved correctly.')
        
    #Funcion de añadir del boton Add
    def add_data(self):
        #Solicitamos al usuario los nuevos datos a través de un cuadro de diálogo de entrada de texto multilineal (para añadir mas de 1 valor)
        nuevos_datos, Aceptar = QInputDialog.getMultiLineText(self, 'Add data', 'Enter the new Channel, Link and Category (One per line):')

        #Si el usuario pulsó "Aceptar" en el cuadro de diálogo
        if Aceptar:
            #Separamos los datos introducidos por líneas
            lista_datos = nuevos_datos.split('\n')

            #Añadimos cada dato en una fila de la tabla enumerate se utiliza para obtener tanto el valor como el índice de un elemento de una secuencia.
            for i, data in enumerate(lista_datos):
                datos = QTableWidgetItem(data)
                self.table.setItem(i, 0, datos)
            
            
                
#Estas 4 líneas hacen posible que se ejecute y muestre la ventana
app = QApplication([])
window = Window()
window.show()
app.exec_()