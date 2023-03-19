#Librerías generales
import sys, re, os
from PyQt5 import QtCore, QtGui, QtWidgets  #Módulos de PyQt5 que usaremos para la GUI
from difflib import SequenceMatcher
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
        self.searchButton = QPushButton('Search channel', self.centralWidget)
        self.searchButton.setGeometry(QRect(200, 20, 160, 30))
        self.searchButton.clicked.connect(self.showWindowSearch)

        #El botón de filtrar
        self.filterButton = QPushButton('Filter by category', self.centralWidget)
        self.filterButton.setGeometry(QRect(380, 20, 160, 30))
        self.filterButton.clicked.connect(self.showWindowFilter)

        #El botón de llenar
        self.fillButton = QPushButton('Fill table', self.centralWidget)
        self.fillButton.setGeometry(QRect(560, 20, 160, 30))
        self.fillButton.clicked.connect(lambda: self.tableWidget.setRowCount(0))
        self.fillButton.clicked.connect(lambda: self.fillTable(channelList))
    
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
        editAction=QAction('Edit', self)
        editAction.triggered.connect(lambda: self.on_buttonEdit_clicked())
        tablesMenu.addAction(deleteAction)
        tablesMenu.addAction(editAction)
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
    
    #Accion del botón de editar
    def on_buttonEdit_clicked(self):
        indexChannel=0 #Indice del canal dentro de la lista 
        selected_row=self.tableWidget.currentRow()
        for indexChnnl in range(len(channelList)):
            second_cell = self.tableWidget.item(selected_row, 1)
            channelName=second_cell.text()
            if (channelList[indexChnnl][1]==channelName): #Compara por URL, ya que esta no se puede repetir
                indexChannel=indexChnnl

        self.secondary_window = WindowEdit(indexChannel)
        self.secondary_window.exec_()

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
        self.inputChannel.setPlaceholderText("Example")
        labelLink = QLabel("Channel URL:")
        self.inputLink = QLineEdit()
        self.inputLink.setPlaceholderText("https://www.youtube.com/@Example")
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

        self.inputChannel.setFocus() #Establece foco en el input
    
    #Método para añadir funcionalidad al botón de añadir
    def addRow(self):
        #Obtenemos los datos de los widgets
        channel=self.inputChannel.text()
        link=self.inputLink.text()
        category=self.comboCategory.currentText()

        #Validamos la entrada del link
        urlYouTube = re.compile(r'^https://www.youtube.com/*')
        if re.match(urlYouTube, link):
            notRepeted=True
            for channelIn in channelList:
                if((link==channelIn[1])):
                    notRepeted=False
                    msgBox=QMessageBox()
                    msgBox.setIcon(QMessageBox.Information)
                    msgBox.setGeometry(350, 350, 0, 0)
                    msgBox.setText('This URL already exists')
                    msgBox.setStandardButtons(QMessageBox.Close)
                    msgBox.setWindowModality(Qt.ApplicationModal)
                    msgBox.exec_()
            if notRepeted:
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
        labelChannel=QLabel("What's the channel name that you want to search?")
        self.inputChannel=QLineEdit()
        self.inputChannel.setPlaceholderText("Enter the name of the channel to search")
        boton=QPushButton("Search", self)
        boton.clicked.connect(self.searchRow)

        # Agregamos los widgets al layout vertical (diseño vertical)
        layout = QVBoxLayout()
        layout.addWidget(labelChannel)
        layout.addWidget(self.inputChannel)
        layout.addWidget(boton)
        self.setLayout(layout) #Establecer layout en la ventana
        
        self.inputChannel.setFocus() #Establece foco en el input
    
    #Método para añadir funcionalidad al botón de buscar
    def searchRow(self):
        channelName=self.inputChannel.text()#Obtenemos el nombre ingresado
        found=True
        for indexChannel in range(len(channelList)):
            #Comparamos las cadenas con el nombre del canal (no sin antes pasarlas a minúsculas con .lower()), esto gracias a una clase de la librería difflib que compara pares de secuencia de entrada
            matcher=SequenceMatcher(None, channelList[indexChannel][0].lower(), channelName.lower()) #Devuelve un valor de semejanza entre 0 y 1, donde 1 significa una coincidencia exacta
            similarity = matcher.ratio() #Calcular la relación de similitud
            if similarity >= 0.7: #Si está por encima del umbral (threshold)
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
        #self.setGeometry(350, 250, 400, 120)
        self.setFixedSize(400, 120)
        self.move(350, 250)
        self.setWindowIcon(QtGui.QIcon('img/fortilogo.png'))
        
        #Vamos a tener una nueva lista con las categorías actualmente disponibles en la tabla
        currentCategoryList=[]
        for channel in channelList:
            if channel[2] in currentCategoryList: #Para no repetir categorías
                continue
            currentCategoryList.append(channel[2])

        #Widgets de la ventana
        labelCategory = QLabel("Filter by:")
        self.comboCategory = QComboBox()
        self.comboCategory.addItems(currentCategoryList)
        boton = QPushButton("Filter", self)
        boton.clicked.connect(self.filterCategory)

        # Agregamos los widgets al layout vertical (diseño vertical)
        layout = QVBoxLayout()
        layout.addWidget(labelCategory)
        layout.addWidget(self.comboCategory)
        layout.addWidget(boton)
        self.setLayout(layout) #Establecer layout en la ventana
    
    #Método para añadir funcionalidad al botón de filtrar
    def filterCategory(self):
        channelCategory=self.comboCategory.currentText() #Obtenemos categoría
        filtredList=[]
        for indexChannel in range(len(channelList)):
            if (channelList[indexChannel][2]==channelCategory):
                channelMatched=channelList[indexChannel]
                filtredList.append(channelMatched)
                window.tableWidget.setRowCount(0) #Limpiar tabla
                window.fillTable(filtredList) #Poner en la tabla el canal
                self.close()

#Clase de la ventana para editar canal
class WindowEdit(QDialog):
    def __init__(self, indexChannel):
        super().__init__()

        self.editList=channelList[indexChannel] #Lista que editaremos, la cual se remplazará al final
        self.indexChannel=indexChannel #Establecemos este dato en la instancia para acceder desde editRow()

        #Configuración de la ventana
        self.setWindowTitle('Edit channel')
        self.setGeometry(100, 100, 600, 300)
        self.setFixedSize(600, 300)
        self.move(300, 200)
        self.setWindowIcon(QtGui.QIcon('img/fortilogo.png'))
        
        #Widgets de la ventana
        labelChannel=QLabel("New channel name:")
        self.inputChannel=QLineEdit()
        self.inputChannel.setPlaceholderText("Example")
        self.inputChannel.setText(self.editList[0])
        labelLink=QLabel("New channel URL:")
        self.inputLink=QLineEdit()
        self.inputLink.setPlaceholderText("https://www.youtube.com/@Example")
        self.inputLink.setText(self.editList[1])
        labelCategory=QLabel("New channel category:")
        self.comboCategory=QComboBox()
        self.comboCategory.addItems(categoryList) #Añadimos la lista de las categorías al comboBox
        currentIndex=categoryList.index(self.editList[2])
        self.comboCategory.setCurrentIndex(currentIndex)
        boton=QPushButton("Add edit", self)
        boton.clicked.connect(self.editRow)

        # Agregamos los widgets al layout vertical (diseño vertical)
        layout=QVBoxLayout()
        layout.addWidget(labelChannel)
        layout.addWidget(self.inputChannel)
        layout.addWidget(labelLink)
        layout.addWidget(self.inputLink)
        layout.addWidget(labelCategory)
        layout.addWidget(self.comboCategory)
        layout.addWidget(boton)
        self.setLayout(layout) #Establecer layout en la ventana

        self.inputChannel.setFocus() #Establece foco en el input
        self.inputChannel.selectAll() #Selecciona todo el texto del input
    
    #Método para añadir funcionalidad al botón de añadir
    def editRow(self):
        #Obtenemos los datos de los widgets
        channel=self.inputChannel.text()
        link=self.inputLink.text()
        category=self.comboCategory.currentText()

        #Validamos la entrada del link
        urlYouTube = re.compile(r'^https://www.youtube.com/*')
        if re.match(urlYouTube, link):
            notRepeted=True
            for channelIn in channelList:
                if((link==channelIn[1])&(channelList.index(channelIn)==self.indexChannel)):
                    pass
                if((link==channelIn[1])&(channelList.index(channelIn)!=self.indexChannel)):
                    notRepeted=False
                    msgBox=QMessageBox()
                    msgBox.setIcon(QMessageBox.Information)
                    msgBox.setGeometry(350, 350, 0, 0)
                    msgBox.setText('This URL already exists')
                    msgBox.setStandardButtons(QMessageBox.Close)
                    msgBox.setWindowModality(Qt.ApplicationModal)
                    msgBox.exec_()
            if notRepeted:
                newChannel=[channel, link, category]
                if(newChannel==self.editList):
                    msgBox=QMessageBox()
                    msgBox.setIcon(QMessageBox.Information)
                    msgBox.setGeometry(350, 350, 0, 0)
                    msgBox.setText('¡No channel changes applied!')
                    msgBox.setStandardButtons(QMessageBox.Close)
                    msgBox.setWindowModality(Qt.ApplicationModal)
                    msgBox.exec_()
                else:
                    #Remplazamos la lista del índice con los datos obtenidos
                    channelList[self.indexChannel][0]=channel
                    channelList[self.indexChannel][1]=link
                    channelList[self.indexChannel][2]=category
                    window.tableWidget.setRowCount(0) #Limpiar tabla
                    overrideTxt()
                    window.fillTable(channelList) #Llenar nuevamente
                    self.close()
        else:
            msgBox=QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setGeometry(350, 350, 0, 0)
            msgBox.setText('The link must be from youtube.com. It should start like this:\n"https://www.youtube.com/"')
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