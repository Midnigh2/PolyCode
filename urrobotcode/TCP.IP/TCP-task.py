import sys
import time
import threading
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from pymodbus.client import ModbusTcpClient


client = ModbusTcpClient(host = '192.168.213.79', port = 502)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.resize(600, 456)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(500, 20, 81, 241))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.btn_1 = QPushButton(Dialog)
        self.btn_1.setObjectName(u"btn_1")
        self.btn_1.setGeometry(QRect(20, 140, 90, 23))
        self.btn_2 = QPushButton(Dialog)
        self.btn_2.setObjectName(u"btn_2")
        self.btn_2.setGeometry(QRect(20, 210, 90, 23))
        self.btn_3 = QPushButton(Dialog)
        self.btn_3.setObjectName(u"btn_3")
        self.btn_3.setGeometry(QRect(20, 280, 90, 23))
        self.btn_4 = QPushButton(Dialog)
        self.btn_4.setObjectName(u"btn_4")
        self.btn_4.setGeometry(QRect(20, 350, 90, 23))
        self.label1 = QLabel(Dialog)
        self.label1.setObjectName(u"label1")
        self.label1.setGeometry(QRect(230, 150, 60, 60))
        self.label1.setScaledContents(True)
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.label1.setIndent(-1)
        self.label2 = QLabel(Dialog)
        self.label2.setObjectName(u"label2")
        self.label2.setGeometry(QRect(410, 150, 60, 60))
        self.label2.setScaledContents(True)
        self.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.label2.setIndent(-1)
        self.label3 = QLabel(Dialog)
        self.label3.setObjectName(u"label3")
        self.label3.setGeometry(QRect(230, 310, 60, 60))
        self.label3.setScaledContents(True)
        self.label3.setAlignment(QtCore.Qt.AlignCenter)
        self.label3.setIndent(-1)
        self.label4 = QLabel(Dialog)
        self.label4.setObjectName(u"label4")
        self.label4.setGeometry(QRect(410, 310, 60, 60))
        self.label4.setScaledContents(True)
        self.label4.setAlignment(QtCore.Qt.AlignCenter)
        self.label4.setIndent(-1)
        self.label1 = QLabel(Dialog)
        self.label1.setObjectName(u"label1")
        self.label1.setGeometry(QRect(230, 150, 60, 60))
        self.label1.setScaledContents(True)
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.label1.setIndent(-1)
        self.label2 = QLabel(Dialog)
        self.label2.setObjectName(u"label2")
        self.label2.setGeometry(QRect(410, 150, 60, 60))
        self.label2.setScaledContents(True)
        self.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.label2.setIndent(-1)
        self.label3 = QLabel(Dialog)
        self.label3.setObjectName(u"label3")
        self.label3.setGeometry(QRect(230, 310, 60, 60))
        self.label3.setScaledContents(True)
        self.label3.setAlignment(QtCore.Qt.AlignCenter)
        self.label3.setIndent(-1)
        self.label4 = QLabel(Dialog)
        self.label4.setObjectName(u"label4")
        self.label4.setGeometry(QRect(410, 310, 60, 60))
        self.label4.setScaledContents(True)
        self.label4.setAlignment(QtCore.Qt.AlignCenter)
        self.label4.setIndent(-1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.label1.setPixmap(QtGui.QPixmap("Red.png"))
        self.label2.setPixmap(QtGui.QPixmap("Red.png"))
        self.label3.setPixmap(QtGui.QPixmap("Red.png"))
        self.label4.setPixmap(QtGui.QPixmap("Red.png"))

        self.btn_1.clicked.connect(self.btn1function_clicked)
        self.btn_2.clicked.connect(self.btn2function_clicked)
        self.btn_3.clicked.connect(self.btn3function_clicked)
        self.btn_4.clicked.connect(self.btn4function_clicked)

        t = threading.Thread(target=myWindow.check, args=())
        t.start()

    def btn1function_clicked(self):
        client.write_register(128, 1)
        self.label1.setPixmap(QtGui.QPixmap("Blue.png"))
    def btn2function_clicked(self):
        client.write_register(128, 2)
        self.label2.setPixmap(QtGui.QPixmap("Blue.png"))
    def btn3function_clicked(self):
        client.write_register(128, 3)
        self.label3.setPixmap(QtGui.QPixmap("Blue.png"))
    def btn4function_clicked(self):
        client.write_register(128, 4)
        self.label4.setPixmap(QtGui.QPixmap("Blue.png"))

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtCore.QCoreApplication.translate("Dialog", "Dialog", None))
        self.btn_1.setText(QtCore.QCoreApplication.translate("Dialog", "Position1", None))
        self.btn_2.setText(QtCore.QCoreApplication.translate("Dialog", "Position2", None))
        self.btn_3.setText(QtCore.QCoreApplication.translate("Dialog", "Position3", None))
        self.btn_4.setText(QtCore.QCoreApplication.translate("Dialog", "Position4", None))


    def check(self):
        while True:
            read1 = client.read_holding_registers(128, 1).registers[0]
            read2 = client.read_holding_registers(130, 1).registers[0]
            if read1 == read2:
                if read1 == 1:
                    self.label1.setPixmap(QtGui.QPixmap("Green.png"))
                    self.label2.setPixmap(QtGui.QPixmap("Red.png"))
                    self.label3.setPixmap(QtGui.QPixmap("Red.png"))
                    self.label4.setPixmap(QtGui.QPixmap("Red.png"))
                elif read1 == 2:
                    self.label2.setPixmap(QtGui.QPixmap("Green.png"))
                    self.label1.setPixmap(QtGui.QPixmap("Red.png"))
                    self.label3.setPixmap(QtGui.QPixmap("Red.png"))
                    self.label4.setPixmap(QtGui.QPixmap("Red.png"))
                elif read1 == 3:
                    self.label3.setPixmap(QtGui.QPixmap("Green.png"))
                    self.label1.setPixmap(QtGui.QPixmap("Red.png"))
                    self.label2.setPixmap(QtGui.QPixmap("Red.png"))
                    self.label4.setPixmap(QtGui.QPixmap("Red.png"))
                elif read1 == 4:
                    self.label4.setPixmap(QtGui.QPixmap("Green.png"))
                    self.label1.setPixmap(QtGui.QPixmap("Red.png"))
                    self.label2.setPixmap(QtGui.QPixmap("Red.png"))
                    self.label3.setPixmap(QtGui.QPixmap("Red.png"))
                else:
                    pass
            time.sleep(1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    myWindow = Ui_Dialog()
    myWindow.setupUi(Dialog)
    Dialog.show()

    app.exec_()
    client.close()
