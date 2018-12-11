import sys
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, \
    QPushButton, QHBoxLayout
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QLCDNumber, QLabel, QLineEdit, QMainWindow
from PyQt5.QtGui import QPixmap
from PIL import Image
#numpy
class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('project.ui', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Pythonshop v1.0')
        self.beginButton.clicked.connect(self.showPic)
        self.rorateLeft.clicked.connect(self.rorateL)
        self.filtrBlack.clicked.connect(self.blackFiltr)
    def showPic(self):
        self.name, self.okBtnPressed = QInputDialog.getText(
            self, "Ввод", "Введите имя файла"
        )
        if self.okBtnPressed:
            pixmap = QPixmap(self.name)
            pixmap = pixmap.scaled(511, 311, QtCore.Qt.KeepAspectRatio)
            self.picture.setPixmap(pixmap)

    def blackFiltr(self):
        pass

    def rorateL(self):
        im = Image.open(self.name)
        im.save(self.name)
        pixmap = QPixmap(self.name)
        pixmap = pixmap.scaled(511, 311, QtCore.Qt.KeepAspectRatio)
        self.picture.setPixmap(pixmap)

app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())