import sys
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, \
    QPushButton, QHBoxLayout
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QSlider
from PyQt5.QtWidgets import QLabel, QLineEdit, QMainWindow
from PyQt5.QtGui import QPixmap, QIcon
from PIL import Image, ImageDraw
from PyQt5.QtCore import Qt
import numpy as np
import os


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('project.ui', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Pythonshop v1.0')
        self.setWindowIcon(QIcon('icon.png'))
        self.name = None

        #Устанавливаем цвета кнопок
        self.beginButton.setStyleSheet(
            "background-color: {}".format('#FFCC00'))
        self.saveButton.setStyleSheet(
            "background-color: {}".format('#FFCC00'))
        self.filtrOriginal.setStyleSheet(
            "background-color: {}".format('#FFCC00'))

        self.rotateLeft.setStyleSheet(
            "background-color: {}".format('#CC0605'))
        self.rotateRight.setStyleSheet(
            "background-color: {}".format('#CC0605'))

        self.beginButton.clicked.connect(self.openFileNameDialog)
        self.saveButton.clicked.connect(self.savePic)

        self.rotateLeft.clicked.connect(self.rotateL)
        self.rotateRight.clicked.connect(self.rotateR)

        self.transfLR.clicked.connect(self.transferfLeftRight)
        self.transUD.clicked.connect(self.transferfUpDown)

        self.brightness.setMinimum(-100)
        self.brightness.setMaximum(100)
        self.brightness.setValue(-100)
        self.brightness.setTickPosition(QSlider.TicksBelow)
        self.brightness.setTickInterval(50)
        self.brightness.valueChanged.connect(self.valueChangeBr)

        self.noise.setMinimum(0)
        self.noise.setMaximum(100)
        self.noise.setValue(0)
        self.noise.setTickPosition(QSlider.TicksBelow)
        self.noise.setTickInterval(50)

        self.saturation.setMinimum(-100)
        self.saturation.setMaximum(100)
        self.saturation.setValue(-100)
        self.saturation.setTickPosition(QSlider.TicksBelow)
        self.saturation.setTickInterval(50)

        self.filtrBlack.clicked.connect(self.blackFiltr)
        self.filtrOriginal.clicked.connect(self.originalFiltr)
        self.filtrRetro.clicked.connect(self.retroFiltr)
        self.filtrNegativ.clicked.connect(self.negativFiltr)

    #Слайдер для яркости изображения
    def valueChangeBr(self):
        k = self.brightness.value()
        image = Image.open(self.name)
        draw = ImageDraw.Draw(image)
        width = image.size[0]
        height = image.size[1]
        pix = image.load()
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0] + k
                b = pix[i, j][1] + k
                c = pix[i, j][2] + k
                if a < 0:
                    a = 0
                if b < 0:
                    b = 0
                if c < 0:
                    c = 0
                if a > 255:
                    a = 255
                if b > 255:
                    b = 255
                if c > 255:
                    c = 255
                draw.point((i, j), (a, b, c))
        image.save(self.name)
        pixmap = QPixmap(self.name)
        pixmap = pixmap.scaled(511, 331, QtCore.Qt.KeepAspectRatio)
        self.picture.setPixmap(pixmap)

    #Обработка нажатий клавиш
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            self.rotateL()
        if event.key() == Qt.Key_D:
            self.rotateR()

    #Открываем картинку
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if self.name:
            self.nameCopy = self.name
            image = Image.open(self.name)
            self.original = image.copy()
            image.save(self.nameCopy)
            self.name = self.name[:self.name.index('.')] + '_copy' + self.name[self.name.index('.'):]
            image.save(self.name)
            pixmap = QPixmap(self.name)
            pixmap = pixmap.scaled(511, 331, QtCore.Qt.KeepAspectRatio)
            self.picture.setPixmap(pixmap)

    #Черно-белый фильтр
    def blackFiltr(self):
        if self.name:
            img = Image.open(self.name)
            arr = np.asarray(img, dtype='uint8')
            x, y, _ = arr.shape

            k = np.array([[[0.2989, 0.587, 0.114]]])
            arr2 = np.round(np.sum(arr * k, axis=2)).astype(np.uint8).reshape((x, y))

            img2 = Image.fromarray(arr2)
            img2.save(self.name)
            pixmap = QPixmap(self.name)
            pixmap = pixmap.scaled(511, 331, QtCore.Qt.KeepAspectRatio)
            self.picture.setPixmap(pixmap)


    #Возвращение оригинального цвета фото
    def originalFiltr(self):
        if self.name:
            if self.original:
                self.original.save(self.name)
                pixmap = QPixmap(self.name)
                pixmap = pixmap.scaled(511, 331, QtCore.Qt.KeepAspectRatio)
                self.picture.setPixmap(pixmap)

    #Ретро фильтр
    def retroFiltr(self):
        if self.name:
            image = Image.open(self.name)
            draw = ImageDraw.Draw(image)
            width = image.size[0]
            height = image.size[1]
            pix = image.load()
            k = 30
            for i in range(width):
                for j in range(height):
                    a = pix[i, j][0]
                    b = pix[i, j][1]
                    c = pix[i, j][2]
                    S = (a + b + c) // 3
                    a = S + k * 2
                    b = S + k
                    c = S
                    if a > 255:
                        a = 255
                    if b > 255:
                        b = 255
                    if c > 255:
                        c = 255
                    draw.point((i, j), (a, b, c))
            del draw
            image.save(self.name)
            pixmap = QPixmap(self.name)
            pixmap = pixmap.scaled(511, 331, QtCore.Qt.KeepAspectRatio)
            self.picture.setPixmap(pixmap)

    #Фильтр Негатив
    def negativFiltr(self):
        if self.name:
            image = Image.open(self.name)
            draw = ImageDraw.Draw(image)
            width = image.size[0]
            height = image.size[1]
            pix = image.load()
            for i in range(width):
                for j in range(height):
                    a = pix[i, j][0]
                    b = pix[i, j][1]
                    c = pix[i, j][2]
                    draw.point((i, j), (255 - a, 255 - b, 255 - c))
            del draw
            image.save(self.name)
            pixmap = QPixmap(self.name)
            pixmap = pixmap.scaled(511, 331, QtCore.Qt.KeepAspectRatio)
            self.picture.setPixmap(pixmap)

    #Поворот налево
    def rotateL(self):
        if self.name:
            im = Image.open(self.name)
            im = im.transpose(Image.ROTATE_90)
            im.save(self.name)
            pixmap = QPixmap(self.name)
            pixmap = pixmap.scaled(511, 331, QtCore.Qt.KeepAspectRatio)
            self.picture.setPixmap(pixmap)

    # Поворот направо
    def rotateR(self):
        if self.name:
            im = Image.open(self.name)
            im = im.transpose(Image.ROTATE_270)
            im.save(self.name)
            pixmap = QPixmap(self.name)
            pixmap = pixmap.scaled(511, 331, QtCore.Qt.KeepAspectRatio)
            self.picture.setPixmap(pixmap)

    #Отображение по вертикали
    def transferfLeftRight(self):
        if self.name:
            im = Image.open(self.name)
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
            im.save(self.name)
            pixmap = QPixmap(self.name)
            pixmap = pixmap.scaled(511, 331, QtCore.Qt.KeepAspectRatio)
            self.picture.setPixmap(pixmap)


    #Отображение по горизонтали
    def transferfUpDown(self):
        if self.name:
            im = Image.open(self.name)
            im = im.transpose(Image.FLIP_TOP_BOTTOM)
            im.save(self.name)
            pixmap = QPixmap(self.name)
            pixmap = pixmap.scaled(511, 331, QtCore.Qt.KeepAspectRatio)
            self.picture.setPixmap(pixmap)

    #Сохранение результата
    def savePic(self):
        if self.name:

            im = Image.open(self.name)
            im.save(self.nameCopy)
            os.remove(self.name)


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())

'''self.sl = QSlider(Qt.Horizontal)
        self.sl.setMinimum(10)
        self.sl.setMaximum(30)
        self.sl.setValue(20)
        self.sl.setTickPosition(QSlider.TicksBelow)
        self.sl.setTickInterval(5)

        layout.addWidget(self.sl)
        self.sl.valueChanged.connect(self.valuechange)
        self.setLayout(layout)
        self.setWindowTitle("SpinBox demo")

    def valuechange(self):
        size = self.sl.value()'''