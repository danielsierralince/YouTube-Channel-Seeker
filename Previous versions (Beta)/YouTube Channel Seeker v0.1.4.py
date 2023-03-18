#Librerías generales
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QDialog, QVBoxLayout, QTableWidget, QLabel, QLineEdit, QComboBox

categoryList=["Autos y vehículos", "Belleza y estilo", "Ciencia y tecnología", "Comedia", "Deportes", "Educación", "Entretenimiento", "Filmación y animación", "Finanzas y negocios", "Gastronomía", "Juegos", "Mascotas y animales", "Música", "Noticias y política", "ONG y activismo", "Personas y blogs", "Viajes y eventos"]

#La clase de la ventana principal que posteriormente usaremos para instanciar el objeto
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        #Atributos principales
        self.setWindowTitle('YouTube Channel Seeker')
        self.setGeometry(100, 100, 1000, 450)
        self.move(100, 100)
        self.centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralWidget)
        
        #La tabla
        self.tableWidget = QtWidgets.QTableWidget(self.centralWidget)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setColumnWidth(0,200) #Ancho de la columna 1
        self.tableWidget.setColumnWidth(1,498) #Ancho de la columna 1
        self.tableWidget.setColumnWidth(2,200) #Ancho de la columna 1
        self.tableWidget.setHorizontalHeaderLabels(['Channel', 'Link', 'Category'])
        self.tableWidget.setGeometry(QtCore.QRect(50, 70, 900, 350))
        
        #FortiLogo
        pixmap = QtGui.QPixmap('img/fortilogo.png')
        icon = QtGui.QIcon(pixmap)
        self.setWindowIcon(icon)
        #self.setWindowIcon(QtGui.QIcon('img/fortilogo.png'))

        #El botón de añadir
        self.addRowButton = QPushButton('Add channel', self.centralWidget)
        self.addRowButton.setGeometry(QtCore.QRect(50, 20, 100, 30))
        self.addRowButton.clicked.connect(self.showWindowAdd)
        
        #Mostrar la 2nda ventana        
    def showWindowAdd(self):
        self.secondary_window = WindowAdd()
        self.secondary_window.exec_()
        
#Clase de la ventana para añadir canal
class WindowAdd(QDialog):
    def __init__(self):
        super().__init__()

        #Configuración de la ventana
        self.setWindowTitle('Add channel')
        self.setGeometry(100, 100, 600, 300)
        self.move(300, 200)
        
        #Widgets de la ventana
        labelChannel = QLabel("Channel name:")
        inputChannel = QLineEdit()
        labelLink = QLabel("Channel URL:")
        inputLink = QLineEdit()
        labelCategory = QLabel("Channel category:")
        comboCategory = QComboBox()
        comboCategory.addItems(categoryList) #Añadimos la lista de las categorías al comboBox
        boton = QPushButton("Add")
        boton.clicked.connect(self.accept) #Hay que cambiar el método accept (defecto)

        # Agregamos los widgets al layout vertical (diseño vertical)
        layout = QVBoxLayout()
        layout.addWidget(labelChannel)
        layout.addWidget(inputChannel)
        layout.addWidget(labelLink)
        layout.addWidget(inputLink)
        layout.addWidget(labelCategory)
        layout.addWidget(comboCategory)
        layout.addWidget(boton)
        self.setLayout(layout) #Establecer layout en la ventana

#Estas 4 líneas hacen posible que se ejecute y muestre la ventana
app = QApplication([])
window = Window()
window.show()
app.exec_()