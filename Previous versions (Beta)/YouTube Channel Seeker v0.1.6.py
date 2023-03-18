#Librerías generales
from PyQt5 import QtCore, QtGui, QtWidgets #Módulos de PyQt5 que usaremos para la GUI
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QDialog, QVBoxLayout, QTableWidget, QLabel, QLineEdit, QComboBox, QTableWidgetItem, QAbstractItemView,QMessageBox #Indicar algunos módulos de la librería para tener un código más versátil
import sys, re

categoryList=["Cars and vehicles", "Beauty and style", "Science and technology", "Comedy", "Sports", "Education", "Entertainment", "Filming and animation", "Finance and business", "Gastronomy", "Games", "Pets and animals", "Music", "News and politics", "NGOs and activism", "People and blogs", "Travel and events"]
channelList=[]

#Leer .txt y meterlo en la lista de canales
def fillList():
    with open('Channels.txt', "r") as txtFile:
        content=txtFile.read() #Establecemos el objeto '_io.TextIOWrapper' en 'str'
        for line in content.split("\n"): #Dividimos en canales
            data=line.split(",") #Dividimos en los datos de cada canal
            channelList.append(data)
    txtFile.close()
fillList()

#Sobreescribir lista de canales por completo
def overrideList():
    with open('Channels.txt', "w") as txtFile:
        for indexChannel in range(len(channelList)):
            for indexData in range(len(channelList[indexChannel])):
                txtFile.write(channelList[indexChannel][indexData])
                if(indexData!=2):
                    txtFile.write(",")
            #El siguiente condicional es para no generar un \n al final, ya que tendríamos un elemento vacío en la tabla
            if(indexChannel==len(channelList)-1):
                print("", end="")
            else:
                txtFile.write("\n")
    txtFile.close()

#La clase de la ventana principal que posteriormente usaremos para instanciar el objeto
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        #Atributos principales
        self.setWindowTitle('YouTube Channel Seeker')
        self.setGeometry(100, 100, 1000, 450)
        self.setFixedSize(1000, 450)  # Bloquea la ventana para que no se pueda cambiar su tamaño
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
        self.setWindowIcon(QtGui.QIcon('img/fortilogo.png'))

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
            self.tableWidget.setRowHeight(row, 35)
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
        self.setFixedSize(600, 300)
        self.move(300, 200)
        
        #Widgets de la ventana
        labelChannel = QLabel("Channel name:")
        self.inputChannel = QLineEdit()
        labelLink = QLabel("Channel URL:")
        self.inputLink = QLineEdit()
        labelCategory = QLabel("Channel category:")
        self.comboCategory = QComboBox()
        self.comboCategory.addItems(categoryList) #Añadimos la lista de las categorías al comboBox
        boton = QPushButton("Add", self)
        boton.clicked.connect(self.addRow)

        # Agregamos los widgets al layout vertical (diseño vertical)
        layout = QVBoxLayout()
        layout.addWidget(labelChannel)
        layout.addWidget(self.inputChannel)
        layout.addWidget(labelLink)
        layout.addWidget(self.inputLink)
        layout.addWidget(labelCategory)
        layout.addWidget(self.comboCategory)
        layout.addWidget(boton)
        self.setLayout(layout) #Establecer layout en la ventana
    
    #Método para añadir funcionalidad al botón
    def addRow(self):
        #Obtenemos los datos de los widgets
        channel=self.inputChannel.text()
        link=self.inputLink.text()
        category=self.comboCategory.currentText()

        #Validamos la entrada del link
        urlYouTube = re.compile(r'^https://www.youtube.com/*')
        if re.match(urlYouTube, link):
            newChannel=[channel, link, category]
            channelList.append(newChannel) #Agregamos el canal mediante los datos obtenidos
            window.tableWidget.setRowCount(0) #Limpiar tabla
            window.fillTable(channelList) #Llenar nuevamente
            overrideList()
            self.close()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setGeometry(350, 350, 0, 0)
            msgBox.setText('The link must be from youtube.com. It should start like this:\n"https://www.youtube.com/"')
            msgBox.setStandardButtons(QMessageBox.Close)
            msgBox.setWindowModality(QtCore.Qt.ApplicationModal)
            msgBox.exec_()

#Estas 4 líneas hacen posible que se ejecute y muestre la ventana
if __name__ == '__main__': #variable "name" establecida como "main" (línea no obligatoria)
    #__main__ permite que el código dentro del bloque solo se ejecute cuando el archivo Python es ejecutado directamente como un programa, y no cuando se importa como un módulo en otro programa
    #Buena páctica a pesar de que no se importe este módulo (se ejecuta directamente)
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec_()) #Garantizar que todo el código de la aplicación se ejecute y se cierre adecuadamente