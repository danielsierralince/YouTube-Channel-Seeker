#Librerías generales
from PyQt5 import QtCore, QtGui, QtWidgets #Módulos de PyQt5 que usaremos para la GUI
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QDialog, QVBoxLayout, QTableWidget, QLabel, QLineEdit, QComboBox, QTableWidgetItem, QAbstractItemView #Indicar algunos módulos de la librería para tener un código más versátil

categoryList=["Autos y vehículos", "Belleza y estilo", "Ciencia y tecnología", "Comedia", "Deportes", "Educación", "Entretenimiento", "Filmación y animación", "Finanzas y negocios", "Gastronomía", "Juegos", "Mascotas y animales", "Música", "Noticias y política", "ONG y activismo", "Personas y blogs", "Viajes y eventos"]
channelList=[]

#Leer .txt y meterlo en una lista
with open('Channels.txt', "r") as txtFile:
    content=txtFile.read() #Establecemos el objeto '_io.TextIOWrapper' en 'str'
    for line in content.split("\n"): #Dividimos en canales
        data=line.split(",") #Dividimos en los datos de cada canal
        channelList.append(data)
    print(channelList)
txtFile.close()

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
        self.tableWidget=QTableWidget(self.centralWidget)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setColumnWidth(0,200) #Ancho de la columna 1
        self.tableWidget.setColumnWidth(1,475) #Ancho de la columna 1
        self.tableWidget.setColumnWidth(2,200) #Ancho de la columna 1
        self.tableWidget.setHorizontalHeaderLabels(['Channel', 'Link', 'Category'])
        self.tableWidget.setGeometry(QtCore.QRect(50, 70, 900, 350))
        self.fillTable(channelList)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers) #Impide la edición del valor de las celdas
        self.tableWidget.setDragDropOverwriteMode(False) #Evitar que se sobrescriban los datos al arrastrar y soltar
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection) #Solo permite seleccionar una fila a la vez
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows) #Selecciona toda la fila cuando se seleccione un elemento
        
        #FortiLogo
        pixmap = QtGui.QPixmap('img/fortilogo.png')
        icon = QtGui.QIcon(pixmap)
        self.setWindowIcon(icon)
        #self.setWindowIcon(QtGui.QIcon('img/fortilogo.png'))

        #El botón de añadir
        self.addRowButton = QPushButton('Add channel', self.centralWidget)
        self.addRowButton.setGeometry(QtCore.QRect(50, 20, 100, 30))
        self.addRowButton.clicked.connect(self.showWindowAdd)
    
    #Llenar la tabla
    def fillTable(self, list):
        row=0
        for channel in list:
            column=0
            self.tableWidget.insertRow(row)
            for data in channel:
                cell=QTableWidgetItem(str(data))
                self.tableWidget.setItem(row, column, cell)
                column+=1
            row+=1

    #Mostrar ventana añadir
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