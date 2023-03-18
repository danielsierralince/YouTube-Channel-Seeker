#Librerías generales
from PyQt5 import QtCore, QtGui, QtWidgets

#La clase de la ventana principal que posteriormente usaremos para instanciar el objeto
class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        #Atributos principales
        self.setWindowTitle('YouTube Channel Seeker')
        self.setGeometry(100, 100, 1000, 450)
        self.centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralWidget)

        #FortiLogo
        pixmap = QtGui.QPixmap('img/fortilogo.png')
        icon = QtGui.QIcon(pixmap)
        self.setWindowIcon(icon)
        #self.setWindowIcon(QtGui.QIcon('img/fortilogo.png'))

        #El botón de añadir
        self.addRowButton = QtWidgets.QPushButton('Add row', self.centralWidget)
        self.addRowButton.setGeometry(QtCore.QRect(50, 20, 100, 30))
        #self.addRowButton.clicked.connect(self.uvkjkb) Lo que va a hacer el botón

        #La tabla
        self.tableWidget = QtWidgets.QTableWidget(self.centralWidget)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setColumnWidth(0,200)
        self.tableWidget.setColumnWidth(1,498)
        self.tableWidget.setColumnWidth(2,200)
        self.tableWidget.setHorizontalHeaderLabels(['Channel', 'Link', 'Category'])
        self.tableWidget.setGeometry(QtCore.QRect(50, 70, 900, 350))

#Estas 4 líneas hacen posible que se ejecute y muestre la ventana
app = QtWidgets.QApplication([])
window = Window()
window.show()
app.exec_()