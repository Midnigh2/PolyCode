import telnetlib
import threading
import time
import sys
from PyQt5 import uic, QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRect


#form
form_class = uic.loadUiType("./dialog.ui")[0]


class Ui_Dialog(object):
    HOST = "192.168.212.220"
    PORT = "7171"

    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(600, 400)
        self.btn_1 = QPushButton(Dialog)
        self.btn_1.setObjectName(u"btn_1")
        self.btn_1.setGeometry(QRect(30, 60, 75, 50))
        self.btn_2 = QPushButton(Dialog)
        self.btn_2.setObjectName(u"btn_2")
        self.btn_2.setGeometry(QRect(30, 130, 75, 50))
        self.btn_3 = QPushButton(Dialog)
        self.btn_3.setObjectName(u"btn_3")
        self.btn_3.setGeometry(QRect(30, 200, 75, 50))
        self.btn_4 = QPushButton(Dialog)
        self.btn_4.setObjectName(u"btn_4")
        self.btn_4.setGeometry(QRect(30, 270, 75, 50))
        self.label1 = QLabel(Dialog)
        self.label1.setObjectName(u"label1")
        self.label1.setEnabled(True)
        self.label1.setGeometry(QRect(190, 110, 71, 71))
        self.label1.setAutoFillBackground(False)
        self.label1.setFrameShape(QFrame.NoFrame)
        self.label1.setScaledContents(True)
        self.label2 = QLabel(Dialog)
        self.label2.setObjectName(u"label2")
        self.label2.setEnabled(True)
        self.label2.setGeometry(QRect(350, 110, 71, 71))
        self.label2.setAutoFillBackground(False)
        self.label2.setFrameShape(QFrame.NoFrame)
        self.label2.setScaledContents(True)
        self.label4 = QLabel(Dialog)
        self.label4.setObjectName(u"label4")
        self.label4.setEnabled(True)
        self.label4.setGeometry(QRect(350, 230, 71, 71))
        self.label4.setAutoFillBackground(False)
        self.label4.setFrameShape(QFrame.NoFrame)
        self.label4.setScaledContents(True)
        self.label3 = QLabel(Dialog)
        self.label3.setObjectName(u"label3")
        self.label3.setEnabled(True)
        self.label3.setGeometry(QRect(190, 230, 71, 71))
        self.label3.setAutoFillBackground(False)
        self.label3.setFrameShape(QFrame.NoFrame)
        self.label3.setScaledContents(True)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(200, 80, 54, 25))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(360, 80, 54, 25))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(360, 200, 54, 25))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(200, 200, 54, 25))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.logoutbtn = QPushButton(Dialog)
        self.logoutbtn.setObjectName(u"logoutbtn")
        self.logoutbtn.setGeometry(QRect(330, 10, 120, 30))
        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(-10, 11, 54, 30))
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(50, 10, 141, 30))
        self.lineEdit.setEchoMode(QLineEdit.Password)
        self.cn_btn = QPushButton(Dialog)
        self.cn_btn.setObjectName(u"cn_btn")
        self.cn_btn.setGeometry(QRect(200, 10, 120, 30))
        self.cur_label = QLabel(Dialog)
        self.cur_label.setObjectName(u"cur_label")
        self.cur_label.setGeometry(QRect(470, 10, 111, 30))
        self.cur_label.setAlignment(QtCore.Qt.AlignCenter)

        self.retranslateUi(Dialog)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.current_position = self
        self.selected_position = self
        self.tn = telnetlib.Telnet(self.HOST, self.PORT)

        self.cn_btn.clicked.connect(self.btn_login)
        self.logoutbtn.clicked.connect(self.logout)
        self.btn_1.clicked.connect(self.btn_goal1)
        self.btn_2.clicked.connect(self.btn_goal2)
        self.btn_3.clicked.connect(self.btn_goal3)
        self.btn_4.clicked.connect(self.btn_goal4)
        self.label1.setPixmap(QtGui.QPixmap("Red.png"))
        self.label2.setPixmap(QtGui.QPixmap("Red.png"))
        self.label3.setPixmap(QtGui.QPixmap("Red.png"))
        self.label4.setPixmap(QtGui.QPixmap("Red.png"))

        self.t1 = threading.Thread(target=myWindow.check, args=())
        self.t1.daemon = True

    def btn_login(self):
        pw = self.lineEdit.text()
        self.password = pw
        self.tn = telnetlib.Telnet(self.HOST, self.PORT)
        self.tn.read_until(b"\n")
        self.tn.write(self.password.encode('ascii') + b'\n')
        self.tn.read_until(b"End of commands")
        self.cur_label.setText("connected")
        self.t1.start()

    def logout(self):
        self.tn.write(b"quit\n")
        time.sleep(1)
        self.close()

    def btn_goal1(self):
        self.tn.write(b"goto goal1\n")
        self.label1.setPixmap(QtGui.QPixmap("Blue.png"))

    def btn_goal2(self):
        self.tn.write(b"goto goal2\n")
        self.label2.setPixmap(QtGui.QPixmap("Blue.png"))

    def btn_goal3(self):
        self.tn.write(b"goto goal3\n")
        self.label3.setPixmap(QtGui.QPixmap("Blue.png"))

    def btn_goal4(self):
        self.tn.write(b"goto goal4\n")
        self.label4.setPixmap(QtGui.QPixmap("Blue.png"))

    def check(self):
        while True:
            time.sleep(1)

            read1 = self.check_status()

            if "Going" in read1:
                print("Going")
            elif "Arrived" in read1:
                if "at Goal1" in read1:
                    self.label1.setPixmap(QtGui.QPixmap("Green.png"))
                    self.label2.setPixmap(QtGui.QPixmap("Red.png"))
                    self.label3.setPixmap(QtGui.QPixmap("Red.png"))
                    self.label4.setPixmap(QtGui.QPixmap("Red.png"))
                    self.current_position = 1
                elif "at Goal2" in read1:
                    self.label2.setPixmap(QtGui.QPixmap("Green.png"))
                    self.label1.setPixmap(QtGui.QPixmap("Red.png"))
                    self.label3.setPixmap(QtGui.QPixmap("Red.png"))
                    self.label4.setPixmap(QtGui.QPixmap("Red.png"))
                    self.current_position = 2
                elif "at Goal3" in read1:
                    self.label3.setPixmap(QtGui.QPixmap("Green.png"))
                    self.label1.setPixmap(QtGui.QPixmap("Red.png"))
                    self.label2.setPixmap(QtGui.QPixmap("Red.png"))
                    self.label4.setPixmap(QtGui.QPixmap("Red.png"))
                    self.current_position = 3
                elif "at Goal4" in read1:
                    self.label4.setPixmap(QtGui.QPixmap("Green.png"))
                    self.label1.setPixmap(QtGui.QPixmap("Red.png"))
                    self.label2.setPixmap(QtGui.QPixmap("Red.png"))
                    self.label3.setPixmap(QtGui.QPixmap("Red.png"))
                    self.current_position = 4

            print("cur_pos" + str(self.current_position))

    def check_status(self):
        self.tn.write("status".encode('ascii') + b'\n')
        cs = self.tn.read_until(b"Status: ")
        cs = self.tn.read_until(b'\n')
        return cs.decode('ascii').strip('\n')

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtCore.QCoreApplication.translate("Dialog", u"Dialog", None))
        self.btn_1.setText(QtCore.QCoreApplication.translate("Dialog", u"goal1", None))
        self.btn_2.setText(QtCore.QCoreApplication.translate("Dialog", u"goal2", None))
        self.btn_3.setText(QtCore.QCoreApplication.translate("Dialog", u"goal3", None))
        self.btn_4.setText(QtCore.QCoreApplication.translate("Dialog", u"goal4", None))
        self.label1.setText("")
        self.label2.setText("")
        self.label4.setText("")
        self.label3.setText("")
        self.label.setText(QtCore.QCoreApplication.translate("Dialog", u"goal1", None))
        self.label_2.setText(QtCore.QCoreApplication.translate("Dialog", u"goal2", None))
        self.label_3.setText(QtCore.QCoreApplication.translate("Dialog", u"goal4", None))
        self.label_4.setText(QtCore.QCoreApplication.translate("Dialog", u"goal3", None))
        self.logoutbtn.setText(QtCore.QCoreApplication.translate("Dialog", u"Disconnect", None))
        self.label_5.setText(QtCore.QCoreApplication.translate("Dialog", u"PW:", None))
        self.cn_btn.setText(QtCore.QCoreApplication.translate("Dialog", u"connect", None))
        self.cur_label.setText("")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    myWindow = Ui_Dialog()
    myWindow.setupUi(Dialog)
    Dialog.show()

    app.exec_()