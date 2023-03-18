#Librerías generales
import sys, re, os
from PyQt5 import QtCore, QtGui, QtWidgets  #Módulos de PyQt5 que usaremos para la GUI
#Indicar algunos módulos de la librería para tener un código más versátil
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QDialog, QVBoxLayout, QTableWidget, QLabel, QLineEdit, QComboBox, QTableWidgetItem, QAbstractItemView,QMessageBox, QMenu, QAction 
from PyQt5.QtCore import QRect, Qt, QUrl
from PyQt5.QtGui import QDesktopServices

current_dir = os.getcwd() # Obtener la ruta de la carpeta actual
os.chdir(current_dir) # Cambiar al directorio actual

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

#Sobreescribir archivo de texto con la lista de canales por completo
def overrideTxt():
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

#Añadir un canal al .txt
def addChannelInTxt(list):
    with open('Channels.txt', "a") as txtFile:
        txtFile.write("\n")
        for dataIndex in range(len(list)):
            txtFile.write(list[dataIndex])
            if(dataIndex!=2):
                txtFile.write(",")

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
        
        #Habilitamos un menú contextual personalizado para QTableWidget (Menú al hacer clic derecho en un elemento)
        #El menú contextual se puede personalizar para adaptarse a las necesidades del usuario y para proporcionar acceso rápido a las opciones de la aplicación
        self.setContextMenuPolicy(Qt.CustomContextMenu) #Establece la política del widget en cuanto a cómo manejar los menús contextuales.
        #Al establecer "CustomContextMenu", se habilita la función "customContextMenuRequested"
        self.customContextMenuRequested.connect(self.show_context_menu) #Se dispara cuando se hace clic derecho en el widget

        #Habilitamos la señal emitida al hacer doble clic en la tabla a la funcion open_link
        self.tableWidget.cellDoubleClicked.connect(self.open_link)

        #FortiLogo
        self.setWindowIcon(QtGui.QIcon('img/fortilogo.png'))

        #El botón de añadir
        self.addRowButton = QPushButton('Add channel', self.centralWidget)
        self.addRowButton.setGeometry(QRect(50, 20, 130, 30))
        self.addRowButton.clicked.connect(self.showWindowAdd)

        #El botón de buscar
        self.addRowButton = QPushButton('Search channel', self.centralWidget)
        self.addRowButton.setGeometry(QRect(200, 20, 160, 30))
        self.addRowButton.clicked.connect(self.showWindowSearch)

        #El botón de filtrar
        self.addRowButton = QPushButton('Filter by category', self.centralWidget)
        self.addRowButton.setGeometry(QRect(380, 20, 160, 30))
        self.addRowButton.clicked.connect(self.showWindowSearch)
    
    #Funcion del doble click para que abra el link del canal
    def open_link(self, row, column):
        # Obtener el enlace de la celda seleccionada
        if column==1:
            link=self.tableWidget.item(row, column).text()
            # Abrir el enlace en un navegador
            QDesktopServices.openUrl(QUrl(link))
    
    #Crear y mostrar menú contextual personalizado
    def show_context_menu(self, pos):
        tablesMenu=QMenu(self) #Menú desplegable
        deleteAction=QAction('Delete', self)
        deleteAction.triggered.connect(lambda: self.on_buttonDelete_clicked())
        tablesMenu.addAction(deleteAction)
        tablesMenu.exec_(self.mapToGlobal(pos)) #Mostrar el menú en la ubicación actual del cursor del ratón (Mapea 'pos')

    #Accion del botón de borrar (primero muestra una ventana de confirmación)
    def on_buttonDelete_clicked(self):
        row=self.tableWidget.currentIndex().row() #Obtener el número de la fila (.row), dado por el índice de la fila seleccionada (.currentIndex)
        
        messageBox = QMessageBox(self)
        messageBox.setIcon(QMessageBox.Question)
        messageBox.setText("¿Are you sure that you want delete this channel?\nChannel name: "+channelList[row][0])
        messageBox.setWindowTitle("Action confirmation")
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        messageBox.setDefaultButton(QMessageBox.No)
        messageBox.buttonClicked.connect(self.handle_confirm_action)
        messageBox.exec_()
    
    #Borrar canal si se confirma la acción
    def handle_confirm_action(self, button):
        indexChannel=0 #Indice del canal dentro de la lista 
        selected_row=self.tableWidget.currentRow()
        for indexChnnl in range(len(channelList)):
            first_cell = self.tableWidget.item(selected_row, 0)
            channelName=first_cell.text()
            if (channelList[indexChnnl][0]==channelName):
                indexChannel=indexChnnl
        if button.text()=="&Yes":
            self.tableWidget.removeRow(selected_row)
            channelList.pop(indexChannel)
            overrideTxt()
        elif button.text()=="&No":
            pass #Acción cancelada

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

    #Mostrar ventana buscar
    def showWindowSearch(self):
        self.secondary_window = WindowSearch()
        self.secondary_window.exec_()
    
    #Mostrar ventana buscar
    def showWindowFilter(self):
        self.secondary_window = WindowFilter()
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
        self.setWindowIcon(QtGui.QIcon('img/fortilogo.png'))
        
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
    
    #Método para añadir funcionalidad al botón de añadir
    def addRow(self):
        #Obtenemos los datos de los widgets
        channel=self.inputChannel.text()
        link=self.inputLink.text()
        category=self.comboCategory.currentText()

        #Validamos la entrada del link
        urlYouTube = re.compile(r'^https://www.youtube.com/*')
        if re.match(urlYouTube, link):
            newChannel=[channel, link, category]
            channelList.append(newChannel) #Agregamos el canal a la lista mediante los datos obtenidos
            addChannelInTxt(newChannel) #Agregamos el canal al archivo de texto
            window.tableWidget.setRowCount(0) #Limpiar tabla
            window.fillTable(channelList) #Llenar nuevamente
            self.close()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setGeometry(350, 350, 0, 0)
            msgBox.setText('The link must be from youtube.com. It should start like this:\n"https://www.youtube.com/"')
            msgBox.setStandardButtons(QMessageBox.Close)
            msgBox.setWindowModality(Qt.ApplicationModal)
            msgBox.exec_()

#Clase de la ventana para buscar canal
class WindowSearch(QDialog):
    def __init__(self):
        super().__init__()

        #Configuración de la ventana
        self.setWindowTitle('Search channel')
        self.setGeometry(350, 250, 400, 150)
        self.setFixedSize(400, 150)
        self.move(350, 250)
        self.setWindowIcon(QtGui.QIcon('img/fortilogo.png'))
        
        #Widgets de la ventana
        labelChannel = QLabel("What's the channel name that you want to search?")
        self.inputChannel = QLineEdit()
        boton = QPushButton("Search", self)
        boton.clicked.connect(self.searchRow)

        # Agregamos los widgets al layout vertical (diseño vertical)
        layout = QVBoxLayout()
        layout.addWidget(labelChannel)
        layout.addWidget(self.inputChannel)
        layout.addWidget(boton)
        self.setLayout(layout) #Establecer layout en la ventana
    
    #Método para añadir funcionalidad al botón de buscar
    def searchRow(self):
        channelName=self.inputChannel.text()#Obtenemos el nombre ingresado
        found=True
        for indexChannel in range(len(channelList)):
            if (channelList[indexChannel][0]==channelName):
                found=False
                channelFound=[channelList[indexChannel]]
                window.tableWidget.setRowCount(0) #Limpiar tabla
                window.fillTable(channelFound) #Poner en la tabla el canal
                self.close()
        if(found):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setGeometry(350, 350, 0, 0)
            msgBox.setText("The channel doesn't exist")
            msgBox.setStandardButtons(QMessageBox.Close)
            msgBox.setWindowModality(Qt.ApplicationModal)
            msgBox.exec_()

#Clase de la ventana para filtrar por categoría
class WindowFilter(QDialog):
    def __init__(self):
        super().__init__()

        #Configuración de la ventana
        self.setWindowTitle('Filter by channel category')
        self.setGeometry(350, 250, 400, 150)
        self.setFixedSize(400, 150)
        self.move(350, 250)
        self.setWindowIcon(QtGui.QIcon('img/fortilogo.png'))
        
        #Widgets de la ventana
        labelChannel = QLabel("What's the channel name that you want to search?")
        self.inputChannel = QLineEdit()
        boton = QPushButton("Search", self)
        boton.clicked.connect(self.searchRow)

        # Agregamos los widgets al layout vertical (diseño vertical)
        layout = QVBoxLayout()
        layout.addWidget(labelChannel)
        layout.addWidget(self.inputChannel)
        layout.addWidget(boton)
        self.setLayout(layout) #Establecer layout en la ventana
    
    #Método para añadir funcionalidad al botón
    def searchRow(self):
        channelName=self.inputChannel.text()#Obtenemos el nombre ingresado
        found=True
        for indexChannel in range(len(channelList)):
            if (channelList[indexChannel][0]==channelName):
                found=False
                channelFound=[channelList[indexChannel]]
                window.tableWidget.setRowCount(0) #Limpiar tabla
                window.fillTable(channelFound) #Poner en la tabla el canal
                self.close()
        if(found):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setGeometry(350, 350, 0, 0)
            msgBox.setText("The channel doesn't exist")
            msgBox.setStandardButtons(QMessageBox.Close)
            msgBox.setWindowModality(Qt.ApplicationModal)
            msgBox.exec_()

#Estas 4 líneas hacen posible que se ejecute y muestre la ventana
if __name__ == '__main__': #variable "name" establecida como "main" (línea no obligatoria)
    #__main__ permite que el código dentro del bloque solo se ejecute cuando el archivo Python es ejecutado directamente como un programa, y no cuando se importa como un módulo en otro programa
    #Buena páctica a pesar de que no se importe este módulo (se ejecuta directamente)
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec_()) #Garantizar que todo el código de la aplicación se ejecute y se cierre adecuadamente