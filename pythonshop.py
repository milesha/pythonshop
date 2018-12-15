import sys
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog, QSlider
from PyQt5.QtWidgets import QMainWindow, QAction, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PIL import Image, ImageDraw, ImageFilter
from PyQt5.QtCore import Qt
import numpy as np
import os


class Pythonshop(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('project.ui', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Pythonshop v1.0')
        self.setWindowIcon(QIcon('icon.png'))
        self.name = None

        # Флаг для корректного сохранения
        self.f = True

        # Флаги для фильтров
        self.negativ = True
        self.black = True

        # Для обработки слайдеров
        self.blur = True
        self.bright = True
        self.details = True
        self.copiesDetail = []
        self.copies = []
        self.copiesBlur = []

        # Обработка закрытия программы
        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)
        menubar = self.menuBar()
        fmenu = menubar.addMenu("File")
        fmenu.addAction(quit)

        # Устанавливаем цвета кнопок
        self.beginButton.setStyleSheet(
            "background-color: {}".format('#FFCC00'))
        self.saveButton.setStyleSheet(
            "background-color: {}".format('#FFCC00'))
        self.filtrOriginal.setStyleSheet(
            "background-color: {}".format('#FFCC00'))

        self.transfLR.setStyleSheet(
            "background-color: {}".format('#FFCC00'))
        self.transUD.setStyleSheet(
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

        # Слайдер затемнения
        self.brightness.setMinimum(0)
        self.brightness.setMaximum(4)
        self.brightness.setValue(0)
        self.brightness.setTickPosition(QSlider.TicksBelow)
        self.brightness.setTickInterval(2)
        self.brightness.valueChanged.connect(self.valueChangeBrightness)

        # Слайдер резкости
        self.sliderDetails.setMinimum(0)
        self.sliderDetails.setMaximum(3)
        self.sliderDetails.setValue(0)
        self.sliderDetails.setTickPosition(QSlider.TicksBelow)
        self.sliderDetails.setTickInterval(2)
        self.sliderDetails.valueChanged.connect(self.valueChangeDetails)

        # Слайдер размытия
        self.blurSlider.setMinimum(0)
        self.blurSlider.setMaximum(4)
        self.blurSlider.setValue(0)
        self.blurSlider.setTickPosition(QSlider.TicksBelow)
        self.blurSlider.setTickInterval(2)
        self.blurSlider.valueChanged.connect(self.valueChangeBlur)

        # Фильтры
        self.filtrBlack.clicked.connect(self.blackFiltr)
        self.filtrOriginal.clicked.connect(self.originalFiltr)
        self.filtrRetro.clicked.connect(self.retroFiltr)
        self.filtrNegativ.clicked.connect(self.negativFiltr)

    # Открываем картинку
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

    # Обработка закрытия программы
    def closeEvent(self, event):
        close = QMessageBox()
        close.setText("Сохранить действия в файле?")
        close.setWindowIcon(QIcon('icon.png'))
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()

        if close == QMessageBox.Yes:
            if not self.f:
                event.accept()
            elif self.name:
                im = Image.open(self.name)
                im.save(self.nameCopy)
                os.remove(self.name)
                event.accept()
        else:
            if not self.f:
                event.accept()
            elif self.name:
                os.remove(self.name)

    # Возвращение оригинального фото
    def originalFiltr(self):
        if self.name:
            if self.original:
                # Возвразаем начальные значения слайдеров
                self.sliderDetails.setValue(0)
                self.blurSlider.setValue(0)
                self.brightness.setValue(0)

                # Отображаем изображение
                self.original.save(self.name)
                pixmap = QPixmap(self.name)
                pixmap = pixmap.scaled(511, 331, QtCore.Qt.KeepAspectRatio)
                self.picture.setPixmap(pixmap)

                # Ставим начальные значения для настроек
                self.negativ = True
                self.black = True
                self.blur = True
                self.bright = True
                self.details = True
                self.copiesDetail = []
                self.copies = []
                self.copiesBlur = []

    # Слайдер для затемнения изображения
    def valueChangeBrightness(self):
        if self.name:
            if self.bright:
                self.copies = []
                image = np.asarray(Image.open(self.name))
                self.copies.append(image)
                for i in range(4):
                    image1 = self.copies[i] // 1.5
                    self.copies.append(image1)
                self.bright = False
                Image.fromarray(np.uint8(self.copies[self.brightness.value()])).save(self.name)
            else:
                Image.fromarray(np.uint8(self.copies[self.brightness.value()])).save(self.name)

            pixmap = QPixmap(self.name)
            pixmap = pixmap.scaled(511, 331, QtCore.Qt.KeepAspectRatio)
            self.picture.setPixmap(pixmap)

    # Слайдер для затемнения изображения
    def valueChangeBlur(self):
        if self.name:
            if self.blur:
                self.copiesBlur = []
                image = np.asarray(Image.open(self.name))
                self.copiesBlur.append(image)
                for i in range(4):
                    image1 = Image.fromarray(np.uint8(self.copiesBlur[i]))
                    im = image1.filter(ImageFilter.GaussianBlur(3))
                    im1 = np.asarray(im)
                    self.copiesBlur.append(im1)
                self.blur = False
                Image.fromarray(np.uint8(self.copiesBlur[self.blurSlider.value()])).save(self.name)
            else:
                Image.fromarray(np.uint8(self.copiesBlur[self.blurSlider.value()])).save(self.name)

            pixmap = QPixmap(self.name)
            pixmap = pixmap.scaled(511, 331, QtCore.Qt.KeepAspectRatio)
            self.picture.setPixmap(pixmap)

    # Слайдер для увеличения резкости
    def valueChangeDetails(self):
        if self.name:
            if self.details:
                image = np.asarray(Image.open(self.name))
                self.copiesDetail.append(image)
                for i in range(3):
                    image1 = Image.fromarray(np.uint8(self.copiesDetail[i]))
                    im = image1.filter(ImageFilter.DETAIL)
                    im1 = np.asarray(im)
                    self.copiesDetail.append(im1)
                self.details = False
                Image.fromarray(np.uint8(self.copiesDetail[self.sliderDetails.value()])).save(self.name)
            else:
                Image.fromarray(np.uint8(self.copiesDetail[self.sliderDetails.value()])).save(self.name)

            pixmap = QPixmap(self.name)
            pixmap = pixmap.scaled(511, 331, QtCore.Qt.KeepAspectRatio)
            self.picture.setPixmap(pixmap)

    # Обработка нажатий клавиш
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            self.rotateL()
        if event.key() == Qt.Key_D:
            self.rotateR()

    # Черно-белый фильтр
    def blackFiltr(self):
        if self.name and self.black:
            # Установка начальных значений для слайдеров
            self.blur = True
            self.bright = True
            self.details = True
            self.copiesDetail = []
            self.copies = []
            self.copiesBlur = []
            self.black = False

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

    # Ретро фильтр
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

            # Установка начальных значений для слайдеров
            self.blur = True
            self.bright = True
            self.details = True
            self.copiesDetail = []
            self.copies = []
            self.copiesBlur = []

            del draw
            image.save(self.name)
            pixmap = QPixmap(self.name)
            pixmap = pixmap.scaled(511, 331, QtCore.Qt.KeepAspectRatio)
            self.picture.setPixmap(pixmap)

    # Фильтр Негатив
    def negativFiltr(self):
        if self.name and self.negativ:
            # Установка начальных значений для слайдеров
            self.blur = True
            self.bright = True
            self.details = True
            self.copiesDetail = []
            self.copies = []
            self.copiesBlur = []
            self.negativ = False

            image = np.asarray(Image.open(self.name))
            Image.fromarray(np.uint8(image * -1)).save(self.name)
            pixmap = QPixmap(self.name)
            pixmap = pixmap.scaled(511, 331, QtCore.Qt.KeepAspectRatio)
            self.picture.setPixmap(pixmap)

    # Поворот налево
    def rotateL(self):
        if self.name:
            self.blur = True
            self.bright = True
            self.details = True
            im = Image.open(self.name)
            im = im.transpose(Image.ROTATE_90)
            im.save(self.name)
            pixmap = QPixmap(self.name)
            pixmap = pixmap.scaled(511, 331, QtCore.Qt.KeepAspectRatio)
            self.picture.setPixmap(pixmap)

    # Поворот направо
    def rotateR(self):
        if self.name:
            self.blur = True
            self.bright = True
            self.details = True
            im = Image.open(self.name)
            im = im.transpose(Image.ROTATE_270)
            im.save(self.name)
            pixmap = QPixmap(self.name)
            pixmap = pixmap.scaled(511, 331, QtCore.Qt.KeepAspectRatio)
            self.picture.setPixmap(pixmap)

    # Отображение по вертикали
    def transferfLeftRight(self):
        if self.name:
            self.blur = True
            self.bright = True
            self.details = True
            im = Image.open(self.name)
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
            im.save(self.name)
            pixmap = QPixmap(self.name)
            pixmap = pixmap.scaled(511, 331, QtCore.Qt.KeepAspectRatio)
            self.picture.setPixmap(pixmap)

    # Отображение по горизонтали
    def transferfUpDown(self):
        if self.name:
            self.blur = True
            self.bright = True
            self.details = True
            im = Image.open(self.name)
            im = im.transpose(Image.FLIP_TOP_BOTTOM)
            im.save(self.name)
            pixmap = QPixmap(self.name)
            pixmap = pixmap.scaled(511, 331, QtCore.Qt.KeepAspectRatio)
            self.picture.setPixmap(pixmap)

    # Сохранение результата
    def savePic(self):
        if self.name:
            self.f = False
            im = Image.open(self.name)
            im.save(self.nameCopy)
            os.remove(self.name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Pythonshop()
    ex.show()
    sys.exit(app.exec())
