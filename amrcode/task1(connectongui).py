import telnetlib
import threading
import time
import sys
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import *

# form
form_class = uic.loadUiType("./dialog.ui")[0]


class main(QMainWindow, form_class):
    HOST = "192.168.212.220"
    PORT = "7171"

    def __init__(self):
        super().__init__()
        self.previous_position = self
        self.current_position = self
        self.selected_point = self

        self.tn = telnetlib.Telnet(self.HOST, self.PORT)
        self.setupUi(self)

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

        self.t1 = threading.Thread(target=self.check, args=())
        self.t1.daemon = True

        self.t2 = threading.Thread(target=self.check_selected_point, args=())
        self.t2.daemon = True

    def btn_login(self):
        pw = self.lineEdit.text()
        self.password = pw
        self.tn = telnetlib.Telnet(self.HOST, self.PORT)
        self.tn.read_until(b"\n")
        self.tn.write(self.password.encode('ascii') + b'\n')
        self.tn.read_until(b"End of commands")
        self.cur_label.setText("connected")
        self.t1.start()
        self.t2.start()

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
            status = self.check_status()
            print("status : " + status)
            if "Going" in status:
                if "to Goal1" in status:
                    self.label1.setPixmap(QtGui.QPixmap("Blue.png"))
                elif "to Goal2" in status:
                    self.label2.setPixmap(QtGui.QPixmap("Blue.png"))
                elif "to Goal3" in status:
                    self.label3.setPixmap(QtGui.QPixmap("Blue.png"))
                elif "to Goal4" in status:
                    self.label4.setPixmap(QtGui.QPixmap("Blue.png"))
            elif "Arrived" in status:
                if "at Goal1" in status:
                    self.current_position = 1
                elif "at Goal2" in status:
                    self.current_position = 2
                elif "at Goal3" in status:
                    self.current_position = 3
                elif "at Goal4" in status:
                    self.current_position = 4

            if self.selected_point == self.current_position:
                if self.selected_point == 1:
                    self.label1.setPixmap(QtGui.QPixmap("Green.png"))
                    self.label2.setPixmap(QtGui.QPixmap("Red.png"))
                    self.label3.setPixmap(QtGui.QPixmap("Red.png"))
                    self.label4.setPixmap(QtGui.QPixmap("Red.png"))
                elif self.selected_point == 2:
                    self.label2.setPixmap(QtGui.QPixmap("Green.png"))
                    self.label1.setPixmap(QtGui.QPixmap("Red.png"))
                    self.label3.setPixmap(QtGui.QPixmap("Red.png"))
                    self.label4.setPixmap(QtGui.QPixmap("Red.png"))
                elif self.selected_point == 3:
                    self.label3.setPixmap(QtGui.QPixmap("Green.png"))
                    self.label1.setPixmap(QtGui.QPixmap("Red.png"))
                    self.label2.setPixmap(QtGui.QPixmap("Red.png"))
                    self.label4.setPixmap(QtGui.QPixmap("Red.png"))
                elif self.selected_point == 4:
                    self.label4.setPixmap(QtGui.QPixmap("Green.png"))
                    self.label1.setPixmap(QtGui.QPixmap("Red.png"))
                    self.label2.setPixmap(QtGui.QPixmap("Red.png"))
                    self.label3.setPixmap(QtGui.QPixmap("Red.png"))

            print("cur_pos : " + str(self.current_position))
            time.sleep(0.1)
    def check_status(self):
        self.tn.write("status".encode('ascii') + b'\n')
        cs = self.tn.read_until(b"Status: ")
        cs = self.tn.read_until(b'\n')
        return cs.decode('ascii').strip('\n')

    def check_selected_point(self):
        while True:
            time.sleep(1)

            read1 = self.check_status()
            if "Going to " in read1:
                if "Goal1" in read1:
                    self.selected_point = 1
                elif "Goal2" in read1:
                    self.selected_point = 2
                elif "Goal3" in read1:
                    self.selected_point = 3
                elif "Goal4" in read1:
                    self.selected_point = 4


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = main()
    dialog.show()

    app.exec_()
