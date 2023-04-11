import telnetlib
import threading
import time
import sys
import numpy as np
import PyQt5.QtWidgets
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import *

# form
form_class = uic.loadUiType("./mapgui.ui")[0]

class main(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.tn = self
        self.rotation = self
        self.setupUi(self)

        self.cn_btn.clicked.connect(self.btn_login)
        self.logoutbtn.clicked.connect(self.logout)
        self.maplabel.setPixmap(QtGui.QPixmap("map.png"))
        self.cur_robot.setPixmap(QtGui.QPixmap("robot.png"))

        self.t1 = threading.Thread(target=self.check, args=())
        self.t1.daemon = True

    def btn_login(self):
        self.HOST = "192.168.212.220"
        self.PORT = "7171"
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

    def check(self):
        while True:
            status = self.check_status().split()
            cur_pos = np.array(status)
            print("x : ", cur_pos[0])
            print("y : ", cur_pos[1])
            print("theta: ", cur_pos[2])

            self.cur_robot.move(int((float(cur_pos[0]) * 0.1)+100), abs(int((float(cur_pos[1]) * 0.1) - 560)))

            #rotate robot icon
            angle = (int(float(cur_pos[2])))
            if angle < 0:
                angle + 360
            self.pixmap = QtGui.QPixmap("robot.png")
            pixmap_rotated = self.pixmap.transformed(QtGui.QTransform().rotate(angle), QtCore.Qt.SmoothTransformation)
            self.cur_robot.setPixmap(pixmap_rotated)

            time.sleep(0.5)

    def check_status(self):
        self.tn.write("status".encode('ascii') + b'\n')
        cs = self.tn.read_until(b"Location: ")
        cs = self.tn.read_until(b'\n')
        return cs.decode('ascii').strip('\n')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = main()
    dialog.show()

    app.exec_()