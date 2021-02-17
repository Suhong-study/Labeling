import os
import sys
import natsort
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Labeling(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_list = []
        self.info_list = []
        self.total_list = []
        self.imagelist2 = []
        self.num = 0
        self.start = QPoint()
        #self.end = QPoint()
        self.pencolor = QColor(255, 0, 0)
        self.setMouseTracking(True)
        self.drawing = False
        self.initUI()

    def initUI(self):
        self.setFixedSize(1000, 600)
        self.setWindowTitle('레이블링프로그램')
        self.setStyleSheet('background-color: white;')
        self.directory_button = QPushButton("디렉터리 선택", self)
        self.directory_button.setFont(QFont("굴림", 15))
        self.directory_button.setGeometry(30, 500, 200, 70)
        self.directory_button.setStyleSheet('background-color: white; border-style: outset;'
                                            ' border-width: 5px; border-color: black;')
        self.directory_button.clicked.connect(self.open)
        self.imagesetting = QLabel(self)
        self.imagesetting.setGeometry(30, 30, 800, 450)
        self.imagesetting.setStyleSheet('background-color: white; border-style: outset; '
                                        'border-width: 5px; border-color: black;')
        self.pathsetting = QLabel(self)
        self.pathsetting.setGeometry(250, 500, 500, 70)
        self.pathsetting.setFont(QFont("굴림", 11))
        self.pathsetting.setStyleSheet('background-color: white; border-style: outset; '
                                       'border-width: 5px; border-color: black;')
        self.left_button = QPushButton("<", self)
        self.left_button.setFont(QFont("굴림", 20))
        self.left_button.setGeometry(770, 500, 90, 70)
        self.left_button.setStyleSheet('background-color: white; border-style: outset; '
                                       'border-width: 5px; border-color: black;')
        self.left_button.clicked.connect(self.preimage)
        self.right_button = QPushButton(">", self)
        self.right_button.setFont(QFont("굴림", 20))
        self.right_button.setGeometry(880, 500, 90, 70)
        self.right_button.setStyleSheet('background-color: white; border-style: outset;'
                                        'border-width: 5px; border-color: black;')
        self.right_button.clicked.connect(self.nextimage)
        self.dog_radio = QRadioButton("Dog", self)
        self.dog_radio.setGeometry(850, 20, 70, 50)
        self.dog_radio.setFont(QFont("굴림", 15))
        self.dog_radio.setChecked(True)
        self.dog_radio.clicked.connect(self.boundingboxcolor)
        self.cat_radio = QRadioButton("Cat", self)
        self.cat_radio.setGeometry(850, 60, 70, 50)
        self.cat_radio.setFont(QFont("굴림", 15))
        self.cat_radio.clicked.connect(self.boundingboxcolor)
        self.dog_color = QLabel(self)
        self.dog_color.setGeometry(936, 32, 25, 25)
        self.dog_color.setStyleSheet('background-color: red;')
        self.cat_color = QLabel(self)
        self.cat_color.setGeometry(936, 72, 25, 25)
        self.cat_color.setStyleSheet('background-color: blue;')

        self.label_info = QLabel(self)
        self.label_info.setFont(QFont("굴림", 15))

        self.imagesetting.mousePressEvent = self.mousePressEvent
        self.imagesetting.mouseMoveEvent = self.mouseMoveEvent
        self.imagesetting.mouseReleaseEvent = self.mouseReleaseEvent
        self.show()

    def open(self):
        self.folder_open = QFileDialog.getExistingDirectory()
        self.folder_open = os.path.realpath(self.folder_open)
        self.image_list = natsort.natsorted(os.listdir(self.folder_open))
        self.pathsetting.setText(self.folder_open)
        self.pixmap = QPixmap(self.imagesetting.width(), self.imagesetting.height())
        self.pixmap.load("{0}\{1}".format(self.folder_open, self.image_list[0]))
        self.num = 0
        self.imagesetting.setPixmap(self.pixmap)
        self.imagesetting.setCursor(Qt.CrossCursor)
        for i in self.image_list:
            if "txt" in i:
                self.image_list.remove(i)
        self.imagelist2 = os.listdir(self.folder_open)
        if self.image_list[self.num].split(".jpg")[0] + ".txt" in self.imagelist2:
            self.loadbounding(self.image_list[self.num].split(".jpg")[0])
        elif self.image_list[self.num].split(".png")[0] + ".txt" in self.imagelist2:
            self.loadbounding(self.image_list[self.num].split(".png")[0])
        elif self.image_list[self.num].split(".jpeg")[0] + ".txt" in self.imagelist2:
            self.loadbounding(self.image_list[self.num].split(".jpeg")[0])

    def loadbounding(self, txtname):
        list2 = []
        fr = open(f"{self.folder_open}/{txtname}.txt", 'r')
        text = fr.read().split("\n")
        text.pop()  # 마지막 공백 삭제
        for i in range(len(text)):
            list1 = str(text[i]).split(", ")
            list2.append(list1)
        painter = QPainter(self.imagesetting.pixmap())
        painter.setFont(QFont("굴림", 15))
        for i in range(len(list2)):
            if list2[i][4] == "Dog":
                painter.setPen(QPen(QColor(255, 0, 0), 5))
                painter.drawText(int(list2[i][0]), int(list2[i][1]) - 10, "Dog")
            else:
                painter.setPen(QPen(QColor(0, 0, 255), 5))
                painter.drawText(int(list2[i][0]), int(list2[i][1]) - 10, "Cat")
            painter.drawRect(QRectF(int(list2[i][0]), int(list2[i][1]), int(list2[i][2]) - int(list2[i][0]),
                                    int(list2[i][3]) - int(list2[i][1])))
            self.imagesetting.repaint()
        fr.close()

    def preimage(self):
        self.store()
        self.num = self.num - 1
        if self.num < 0:
            QMessageBox.about(self, "알림", "첫번째 이미지입니다.")
            self.num = 0
        else:
            self.imagelist2 = os.listdir(self.folder_open)
            self.pixmap.load("{0}\{1}".format(self.folder_open, self.image_list[self.num]))
            self.imagesetting.setPixmap(self.pixmap)
            self.imagesetting.setCursor(Qt.CrossCursor)
            if self.image_list[self.num].split(".jpg")[0] + ".txt" in self.imagelist2:
                self.loadbounding(self.image_list[self.num].split(".jpg")[0])
            elif self.image_list[self.num].split(".png")[0] + ".txt" in self.imagelist2:
                self.loadbounding(self.image_list[self.num].split(".png")[0])
            elif self.image_list[self.num].split(".jpeg")[0] + ".txt" in self.imagelist2:
                self.loadbounding(self.image_list[self.num].split(".jpeg")[0])

    def nextimage(self):
        self.store()
        self.num = self.num + 1
        if self.num == (len(self.image_list)):
            QMessageBox.about(self, "알림", "마지막 이미지입니다.")
            self.num = self.num - 1
        else:
            self.imagelist2 = os.listdir(self.folder_open)
            self.pixmap.load("{0}\{1}".format(self.folder_open, self.image_list[self.num]))
            self.imagesetting.setPixmap(self.pixmap)
            self.imagesetting.setCursor(Qt.CrossCursor)
            if self.image_list[self.num].split(".jpg")[0] + ".txt" in self.imagelist2:
                self.loadbounding(self.image_list[self.num].split(".jpg")[0])
            elif self.image_list[self.num].split(".png")[0] + ".txt" in self.imagelist2:
                self.loadbounding(self.image_list[self.num].split(".png")[0])
            elif self.image_list[self.num].split(".jpeg")[0] + ".txt" in self.imagelist2:
                self.loadbounding(self.image_list[self.num].split(".jpeg")[0])

    def store(self):
        if len(self.total_list) > 0:
            if ".jpg" in self.image_list[self.num]:
                self.prestore = self.image_list[self.num].split(".jpg")[0]
            elif ".png" in self.image_list[self.num]:
                self.prestore = self.image_list[self.num].split(".png")[0]
            elif ".jpeg" in self.image_list[self.num]:
                self.prestore = self.image_list[self.num].split(".jpeg")[0]
            fw = open(f"{self.folder_open}/{self.prestore}.txt", 'a')
            for i in range(len(self.total_list)):
                self.writestore = self.total_list[i]
                self.writestore = str(self.writestore).replace("[", "")
                self.writestore = str(self.writestore).replace("]", "")
                self.writestore = str(self.writestore).replace("\'", "")
                fw.write(str(self.writestore) + "\n")
            for i in range(len(self.total_list)):
                self.total_list.pop()
            fw.close()

    def boundingboxcolor(self):
        sender = self.sender()
        if sender == self.cat_radio:
            self.pencolor = QColor(0, 0, 255)
        elif sender == self.dog_radio:
            self.pencolor = QColor(255, 0, 0)

    def eraser(self, x, y):
        list2 = []
        list3 = []
        if ".jpg" in self.image_list[self.num]:
            txtname = self.image_list[self.num].split(".jpg")[0]
        elif ".png" in self.image_list[self.num]:
            txtname = self.image_list[self.num].split(".png")[0]
        elif ".jpeg" in self.image_list[self.num]:
            txtname = self.image_list[self.num].split(".jpeg")[0]
        fr = open(f"{self.folder_open}/{txtname}.txt", 'r')
        text = fr.read().split("\n")
        text.pop()  # 마지막 공백 삭제
        for i in range(len(text)):
            list1 = str(text[i]).split(", ")
            list2.append(list1)
        fr.close()
        fd = open(f"{self.folder_open}/{txtname}.txt", 'w')
        for i in range(len(list2)):
            list3.append(list2[i])
        for i in range(len(list2)):
            a, b, c, d = int(list2[i][0]), int(list2[i][2]), int(list2[i][1]), int(list2[i][3])
            if a <= x <= b and c <= y <= d:
                delinfo = list2[i]
                list3.remove(delinfo)
        for i in range(len(list3)):
            writestore = list3[i]
            writestore = str(writestore).replace("[", "")
            writestore = str(writestore).replace("]", "")
            writestore = str(writestore).replace("\'", "")
            fd.write(str(writestore) + "\n")
        fd.close()
        self.pixmap.load("{0}\{1}".format(self.folder_open, self.image_list[self.num]))
        self.imagesetting.setPixmap(self.pixmap)
        self.imagelist2 = os.listdir(self.folder_open)
        if txtname + ".txt" in self.imagelist2:
            self.loadbounding(txtname)

    def mousePressEvent(self, e):
        if e.buttons() & Qt.LeftButton:
            self.drawing = True
            self.start = e.pos()
        elif e.buttons() & Qt.RightButton:
            self.eraser(e.x(), e.y())

    def mouseMoveEvent(self, e):
        if self.drawing:
            newpixmap = self.imagesetting.pixmap()
            newpixmap = newpixmap.copy(0, 0, self.imagesetting.width(), self.imagesetting.height())
            painter = QPainter(self.imagesetting.pixmap())
            painter.setPen(QPen(self.pencolor, 5))
            painter.drawRect(QRect(self.start, e.pos()))
            painter.end()
            # self.update()
            self.imagesetting.repaint()
            self.imagesetting.setPixmap(newpixmap)

    def mouseReleaseEvent(self, e):
        if self.drawing:
            self.drawing = False
            painter = QPainter(self.imagesetting.pixmap())
            painter.setFont(QFont("굴림", 15))
            painter.setPen(QPen(self.pencolor, 5))
            painter.drawRect(QRect(self.start, e.pos()))
            a, b, c, d = self.start.x(), self.start.y(), e.x(), e.y()
            self.info_list = [a, b, c, d]
            if self.pencolor == QColor(255, 0, 0):
                painter.drawText(a, b - 10, "Dog")
                self.info_list.append("Dog")
                self.total_list.append(self.info_list)
            elif self.pencolor == QColor(0, 0, 255):
                painter.drawText(a, b - 10, "Cat")
                self.info_list.append("Cat")
                self.total_list.append(self.info_list)
            self.imagesetting.repaint()
            self.store()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Labeling()
    sys.exit(app.exec_())