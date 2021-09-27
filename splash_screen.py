from PyQt5.uic import loadUi
from PyQt5 import QtCore
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from random import randrange
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QGraphicsRotation, QGraphicsTransform
from PyQt5.uic import loadUi
from PyQt5.uic.properties import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtWidgets import QMainWindow, QLabel, QCheckBox, QWidget
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtCore import Qt, QTimer

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)

        
        # self.showMaximized()
        self.loginbutton.clicked.connect(self.verify_login)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)


    def verify_login(self):
        widget.setWindowFlag(Qt.FramelessWindowHint, False)
        print("login")

class Main(QDialog):
    def __init__(self):
        super(Main, self).__init__()
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        loadUi("login_splash.ui", self)
        self.lbl = QLabel()
        self.gif = QMovie('enimation_splash.gif')
        self.label_2.setMovie(self.gif)
        self.gif.start()

        
        splash_screen_time = randrange(2700, 4500)
        QTimer.singleShot(splash_screen_time, self.database_login)
   
    def database_login(self):
        print("database fun")
        login = Login()
        # widget.setWindowFlag(QtCore.Qt.FramelessWindowHint, False)
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = Main()
    widget = QtWidgets.QStackedWidget()
    widget.setGeometry(400, 100, 600, 415)
    widget.setWindowFlag(QtCore.Qt.FramelessWindowHint, True)
    widget.addWidget(gui)
    widget.show()

    app.exec_()


spashscreen()


# class Main(QDialog):
#     def __init__(self):
#         super().__init__()
#         # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
#         loadUi("login_splash.ui", self)
#         self.lbl = QLabel()
#         self.gif = QMovie('enimation_splash.gif')
#         self.label_2.setMovie(self.gif)
#         self.gif.start()

#         splash_screen_time = randrange(2700, 4500)
#     #     QTimer.singleShot(splash_screen_time, self.database_login)
#     #     # self.show()
#     # def database_login(self):
#     #     print("call database login")

#     #     login = Login()
#     #     # widget.setWindowFlag(Qt.FramelessWindowHint, False)
#     #     widget.addWidget(login)
#     #     widget.setCurrentIndex(widget.currentIndex() + 1)

# def spashscreen():
#     app = QApplication(sys.argv)
#     gui = Main()

#     widget = QtWidgets.QStackedWidget()
#     widget.setWindowFlag(QtCore.Qt.FramelessWindowHint, True)
#     widget.addWidget(gui)
#     widget.show()

#     app.exec_()


# spashscreen()




