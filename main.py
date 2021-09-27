from python_usb_enable_script import unblock_usb, block_usb
from python_software_disable_script import unblock_soft, block_soft
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QHBoxLayout, QPushButton
from waitingspinnerwidget import QtWaitingSpinner
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QGraphicsRotation, QGraphicsTransform
from PyQt5.uic import loadUi
import requests
import threading
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.uic.properties import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import datetime
from PyQt5.QtGui import QColor
import socket
import math
import pickle
import json
from PyQt5 import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2, time
import datetime
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
from win32api import GetSystemMetrics
from PIL import ImageGrab
from pynput.keyboard import Key, Listener
import logging
import time
from datetime import datetime as dt
import sys
import ctypes
import random
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QCheckBox, QWidget
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from nav_button_css import css_active, css_not_active
from ui_functions import *
from PyQt5.QtCore import Qt, QTimer
# from connected_ip import get_ips
from connected_ip import *
import sqlite3
# print(time.time())
# print(randomlist[0])
global_port = [12312]
server_ip_video_thread_flag = False

# CIRCULAR LOADER
loading_counter = 0
class Loading(QDialog):
    def __init__(self):
        super(Loading, self).__init__()
        loadUi("circular_loader.ui", self)
        self.progressBarValue(0)

        ## ==> REMOVE STANDARD TITLE BAR
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Remove title bar
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Set background to transparent

        ## ==> APPLY DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 120))
        self.circularBg.setGraphicsEffect(self.shadow)

        ## QTIMER ==> START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        # TIMER IN MILLISECONDS
        self.timer.start(5)

        self.show()

    def progress(self):
        global loading_counter
        value = loading_counter

        if value >= 100: value = 1.000
        self.progressBarValue(value)

        if loading_counter > 100:
            self.timer.stop()
            self.close()

        loading_counter += 0.5

    def progressBarValue(self, value):

        styleSheet = """
        QFrame{
        	border-radius: 150px;
        	background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255, 0, 127, 0), stop:{STOP_2} rgba(85, 170, 255, 255));
        }
        """
        progress = (100 - value) / 100.0

        stop_1 = str(progress - 0.001)
        stop_2 = str(progress)

        newStylesheet = styleSheet.replace("{STOP_1}", stop_1).replace("{STOP_2}", stop_2)
        self.circularProgress.setStyleSheet(newStylesheet)

# NEW LOADER
class Loader(QDialog):
    def __init__(self):
        super(Loader, self).__init__()

        loadUi("new_loader.ui", self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Remove title bar
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Set background to transparent
        self.lbl = QLabel()
        self.gif = QMovie('new_loader.gif')
        self.label.setMovie(self.gif)
        self.gif.start()
        self.show()

class Example_Window(QDialog):
    def __init__(self):
        super(Example_Window,self).__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)  # Remove title bar
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Set background to transparent
        # QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint
        self.initUI()

    def initUI(self):
        self.spinner = QtWaitingSpinner(self)
        self.spinner.start()
        hbox = QHBoxLayout()
        hbox.addWidget(self.spinner)
        self.setLayout(hbox)
        # frame_12
        # self.show()

# SQLITE DATABASE CONNECT
def connect_database():
    conn = sqlite3.connect("fineoutput_employee.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee (id INTEGER PRIMARY KEY, email text, password text)")
    conn.commit()
    conn.close()


# VIDEO SERVER THREAD
class VideoThread(QThread):
    _running = True

    def __init__(self, port, ip):
        QThread.__init__(self)
        self.video_share_thread_stop = False
        self.send_port = port
        self.send_ip = ip

    change_pixmap_signal = pyqtSignal(np.ndarray)

    def run(self):
        try:

            host_name = socket.gethostname()
            host = self.send_ip
            print("host ip ?? ", host)

            port = self.send_port[0]
            print("video thread port ########### ", port)
            max_length = 65540
            print(host, port)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((host, port))
            frame_info = None
            buffer = None
            frame = None
            print("-> waiting for connection")
            while True:
                data, address = self.sock.recvfrom(max_length)
                if len(data) < 100:
                    frame_info = pickle.loads(data)
                    if frame_info:
                        nums_of_packs = frame_info["packs"]
                        for i in range(nums_of_packs):
                            data, address = self.sock.recvfrom(max_length)
                            if i == 0:
                                buffer = data
                            else:
                                buffer += data
                        frame = np.frombuffer(buffer, dtype=np.uint8)
                        frame = frame.reshape(frame.shape[0], 1)
                        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                        if frame is not None and type(frame) == np.ndarray:
                            self.change_pixmap_signal.emit(frame)
                            if cv2.waitKey(1) == 27:
                                break
            print("goodbye")
        finally:
            print("self.sock.close()")
            self.sock.close()
            print('ended')

    def get_id(self):

        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()

        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

# VIDEO CLIENT THREAD
class Client(threading.Thread):

    def __init__(self, c_t_s):
        threading.Thread.__init__(self)

        self.WIDTH = GetSystemMetrics(0)
        self.HEIGHT = GetSystemMetrics(1)
        self.max_length = 65000
        host_name = socket.gethostname()
        self.host = socket.gethostbyname(host_name)

        # self.port = random.sample(range(12312, 12390), 1)
        print("Client Port For Screen Share", global_port[0])
        global_port[0] = random.sample(range(12312, 12390), 1)

        print("clint randomlist[0] ::", global_port[0][0])
        # print("clint randomlist[0] type ::", type(int(global_port[0])))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.client_thread_stop = c_t_s

    def run(self):
        try:
            while True:

                img = ImageGrab.grab(bbox=(0, 0, self.WIDTH, self.HEIGHT))
                img = np.array(img)
                retval, buffer = cv2.imencode(".jpg", img)

                if retval:
                    buffer = buffer.tobytes()
                    buffer_size = len(buffer)
                    num_of_packs = 1
                    if buffer_size > self.max_length:
                        num_of_packs = math.ceil(buffer_size / self.max_length)
                    frame_info = {"packs": num_of_packs}
                    # self.sock.sendto(pickle.dumps(frame_info), (self.host, self.port))
                    self.sock.sendto(pickle.dumps(frame_info), (self.host, global_port[0][0]))
                    left = 0
                    right = self.max_length

                    for i in range(num_of_packs):
                        data = buffer[left:right]
                        left = right
                        right += self.max_length
                        # self.sock.sendto(data, (self.host, self.port))
                        self.sock.sendto(data, (self.host, global_port[0][0]))
        finally:
            print('ended')

    def get_id(self):

        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

# KEYLOGGER THREAD
class Keyloger(QThread):
    def __init__(self, keyloger_for_decision):
        QThread.__init__(self)
        self.x = datetime.datetime.now()
        self.keyloger_for_decision = keyloger_for_decision
        if keyloger_for_decision == 'TASK':
            self.Task_keyloger_multi_string = ''''''
            # print("keyloger For Task",keyloger_for_decision)
        else:
            self.Attendence_keyloger_multi_string = ''''''
            # print("keyloger For Attendence", keyloger_for_decision)
        self.write_time = int(self.x.strftime("%H") + "" + self.x.strftime("%M") + "" + self.x.strftime("%S"))

    stop_threads = True

    def run(self):
        def on_press(key):
            key = str(key)
            key = key.replace("'", "")
            logging.info(key)
            if key == 'Key.space':
                key = ' '
            if key == 'Key.enter':
                key = '/n'

            file = open('C:\\Users\\keyLog.txt', 'a')
            if self.keyloger_for_decision == 'TASK':

                self.Task_keyloger_multi_string += str(key)
            elif self.keyloger_for_decision == 'Attendence':
                self.Attendence_keyloger_multi_string += str(key)
            else:
                pass

            self.x = datetime.datetime.now()
            self.write_time = int(self.x.strftime("%H") + "" + self.x.strftime("%M") + "" + self.x.strftime("%S"))

            file.write(key)

        def on_release(key):
            if self.stop_threads == False:
                return False

        with Listener(on_press=on_press,
                      on_release=on_release) as listener:
            listener.join()


from PyQt5.QtGui import QMovie
from random import randrange

# TASK CREATE DIALOG
class task_create_dialog(QDialog):
    def __init__(self):
        super(task_create_dialog, self).__init__()
        loadUi("task_create_successfully_2.ui", self)
        self.setWindowTitle("Create Task")
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.show()

# TASK COMPLETE DIALOG
class task_complete_dialog(QDialog):
    def __init__(self):

        super(task_complete_dialog, self).__init__()
        loadUi("task_complete_dialog.ui", self)
        self.setWindowTitle("Task Complete")
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.show()

# ATTENDENCE START DIALOG
class attendence_start_dialog(QDialog):
    def __init__(self):

        super(attendence_start_dialog, self).__init__()
        loadUi("attendence_start_dialog.ui", self)
        self.setWindowTitle("Attendance")
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.show()

# ATTENDENCE START DIALOG RESPONCE MESSAGE
class attendence_start_dialog_responce_message(QDialog):
    def __init__(self):

        super(attendence_start_dialog_responce_message, self).__init__()
        loadUi("attendence_start_dialog_after_responce.ui", self)
        self.setWindowTitle("Attendance")
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.show()

# ATTENDENCE STOP DIALOG RESPONCE MESSAGE
class attendence_stop_dialog_responce_message(QDialog):
    def __init__(self):

        super(attendence_stop_dialog_responce_message, self).__init__()
        loadUi("attendence_stop_dialog_after_responce.ui", self)
        self.setWindowTitle("Attendance")
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.show()

# ATTENDENCE STOP DIALOG
class attendence_stop_dialog(QDialog):
    def __init__(self):

        super(attendence_stop_dialog, self).__init__()
        loadUi("attendence_stop_dialog.ui", self)
        self.setWindowTitle("Attendance")
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.show()

# TASK COMPLETE DIALOG AFTER RESPONCE
class task_complete_dialog_after_responce(QDialog):
    def __init__(self):

        super(task_complete_dialog_after_responce, self).__init__()
        loadUi("task_complete_dialog_after_responce.ui", self)
        self.setWindowTitle("Attendance")
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.show()

# LOGOUT DIALOG
class logout_dialog(QDialog):
    def __init__(self):

        super(logout_dialog, self).__init__()
        loadUi("logout_dialog.ui", self)
        self.setWindowTitle("Logout")
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.show()

# SPLASH SCREEN
class SplashScreen(QDialog):
    def __init__(self):
        super(SplashScreen, self).__init__()

        loadUi("login_splash.ui", self)
        self.lbl = QLabel()
        self.gif = QMovie('enimation_splash.gif')
        self.label_2.setMovie(self.gif)
        self.gif.start()

        # self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
        # self.setWindowFlag(Qt.FramelessWindowHint, True)

        # self.show()
        connect_database()
        splash_screen_time = randrange(2700, 4500)
        # print("splash_screen_time :: ", splash_screen_time)

        # ##########email and password search in database###########

        conn = sqlite3.connect("fineoutput_employee.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM employee")
        self.rows = cur.fetchall()
        conn.close()
        # print("database all entry ::", self.rows)
        # ##########################################################

        if self.rows:
            # print(self.rows[0][1])
            # self.database_login()QTimer.singleShot(splash_screen_time, self.database_login)
            QTimer.singleShot(splash_screen_time, self.database_login)
        else:
            QTimer.singleShot(splash_screen_time, self.login_fun)
            # print("now start")

        # print("time over")

    def database_login(self):
        # print("call database login")
        self.email = self.rows[0][1]
        self.password = self.rows[0][2]
        # url = f'https://www.fineoutput.website/fruitsecom/home/login_api/{self.email}/{self.password}'
        url = f'https://www.fineoutput.us/employee/login/employee_login/{self.email}/{self.password}'
        createacc = CreateAcc(url, self.email, self.password)
        # widget.setWindowFlag(Qt.FramelessWindowHint, False)
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def login_fun(self):

        # print("login class called")
        # widget.setWindowFlag(Qt.FramelessWindowHint, False)

        # widget.show()
        # widget.showMaximized()
        # widget.showMaximized()
        login = Login()

        widget.addWidget(login)
        # widget.showMaximized()

        widget.setCurrentIndex(widget.currentIndex() + 1)

# LOGIN CLASS
class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)

        self.showMaximized()
        self.loginbutton.clicked.connect(self.verify_login)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        # block_usb()
        # block_soft()

    def verify_login(self):
        if len(self.email.text()) > 2 and len(self.password.text()) > 2:
            print("verify if")

            self.loginfunction()
        else:
            self.label.setText("Please Fill UserName And Password")
            self.label.setAlignment(QtCore.Qt.AlignCenter)
            print("login fail")

    def loginfunction(self):
        print("login Button clicked")

        self.email = self.email.text()
        self.password = self.password.text()
        # print(self.email, self.password)

        if self.email:
            # print("Successfully logged in with email: ", self.email, "and password:", self.password)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

            URL = "https://www.fineoutput.us/employee/api/Home/login_api"
            try:

                r = requests.post(url=URL, data={'email': self.email, 'password': self.password}, headers=headers)
                login_succ = r.content.decode('ascii')
                # print("r.content :: ",login_succ )
                # print("r.content :: ", type(login_succ))
                # print("responce for log in:: ", r)
                if login_succ == 'success':
                    print(f"{login_succ} logged in with email: ", self.email, "and password:", self.password)
                    # print("login responce database")
                    # ############ Email and Password insert in database###################
                    conn = sqlite3.connect("fineoutput_employee.db")
                    cur = conn.cursor()
                    cur.execute("INSERT INTO employee VALUES (NULL,?,?)", (self.email, self.password))
                    conn.commit()
                    conn.close()

                    # #####################################################################
                    # print("enterin if block")
                    # url = f'https://www.fineoutput.website/fruitsecom/home/login_api/{self.email}/{self.password}'
                    # url = 'https://www.google.com/'
                    url = f'https://www.fineoutput.us/employee/login/employee_login/{self.email}' \
                          f'/{self.password}'

                    createacc = CreateAcc(url, self.email, self.password)
                    widget.addWidget(createacc)
                    widget.setCurrentIndex(widget.currentIndex() + 1)
                else:

                    print("response wrong")

                    login = Login()
                    login.label.setText("Please Fill Correct Details")
                    login.label.setAlignment(QtCore.Qt.AlignCenter)
                    widget.addWidget(login)
                    widget.setCurrentIndex(widget.currentIndex() + 1)
            except:
                login = Login()
                login.label.setText("Please Check Internet Connection")
                login.label.setAlignment(QtCore.Qt.AlignCenter)
                widget.addWidget(login)
                widget.setCurrentIndex(widget.currentIndex() + 1)


class IpDialog(QDialog):
    def __init__(self):
        super(IpDialog, self).__init__()
        loadUi("ip_dialog.ui", self)
        self.video_thread_port = global_port[0]


class Add_task(QDialog):
    def __init__(self):
        super(Add_task, self).__init__()
        # loadUi("task_add.ui", self)
        loadUi("task_add - Copy.ui", self)
        # self.video_thread_port = global_port[0]

class Add_task_web(QDialog):
    def __init__(self):
        super(Add_task_web, self).__init__()
        # loadUi("task_web_main.ui", self)
        loadUi("task_add.ui", self)
        # self.showMaximized()
        # self.video_thread_port = global_port[0]

class Setting(QDialog):
    def __init__(self):
        super(Setting, self).__init__()
        loadUi("setting_dialog.ui", self)

        self.pwd_frame = False

        self.cancel_Button.clicked.connect(self.cancel)
        self.apply_Button.clicked.connect(self.apply)

        self.usb_checkbox.stateChanged.connect(self.usb_clickBox)
        self.soft_checkbox.stateChanged.connect(self.soft_clickBox)
        self.pass_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_frame.hide()

    def cancel(self):
        # print("cancel button click")
        self.hide()
        # print("cancel button 2 click")

    def apply(self):
        password_us = self.pass_edit.text()
        print("password :: ", password_us)
        if password_us == 'fineoutput':
            unblock_usb()
            unblock_soft()
            self.hide()

    def usb_clickBox(self, state):

        if state == QtCore.Qt.Checked:

            self.password_frame.show()
            print('usb Checked')
        else:
            self.password_frame.hide()
            print('usb Unchecked')

    def soft_clickBox(self, state):

        if state == QtCore.Qt.Checked:
            self.password_frame.show()
            print('soft Checked')
        else:
            self.password_frame.hide()
            print('soft Unchecked')


class CreateAcc(QMainWindow):
    def __init__(self, url, email, password):
        super(CreateAcc, self).__init__()
        # loadUi("createacc_edit_1.ui", self)
        loadUi("side_bar - Copy.ui", self)
        # loadUi("side_bar - Copy - Copy.ui", self)
        self.email = email
        self.password = password
        image_label = self.image_label
        # print(f"login email and password in createAcc class :: {email},{password}")
        self.client_thread_stop = False
        c_t_s = self.client_thread_stop
        self.video_share_thread_stop = False
        self.thread_client = Client(c_t_s)
        self.video_thread_port = global_port[0]
        # print("////////global_port client object ////////", global_port[0])

        self.i = 0
        self.timeer_flag = True
        self.time_count = 0

        self.task_time_count = 0
        self.task_time_start = False
        self.task_complete_flag = False
        self.full_task_name = ''
        self.task_select_flag = False
        self.task_show_flag = False
        self.task_name_total_time_dist = {}
        self.total_task_time = 0
        self.wasted_time = []

        self.count = 1
        self.url = url
        self.time_start = False
        self.web_block = False
        self.web_block_flag = False
        self.string_time = ''
        self.start_button_flag = False
        # self.waste_time=

        self.client_thread_counter = 0
        self.lunch_break_button_handle = ''

        self.browse_window.setUrl(QUrl(self.url))

        # self.left_side_menu.setMaximumWidth(250)
        self.version_button.setEnabled(False)
        self.version_button.setText("Ver 1.0")
        self.version_button.clicked.connect(self.version_btn_fun)

        self.Btn_Toggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 250, True))

        self.home_button.clicked.connect(self.home)
        self.screen_share.clicked.connect(self.screenshare)
        self.attendence_button.clicked.connect(self.attendence)
        self.task_button.clicked.connect(self.task)
        self.setting_button.clicked.connect(self.setting)
        self.setting_button.hide()

        self.logout_button.clicked.connect(self.logout)

        self.home_button.setStyleSheet(css_active)
        self.screen_share.setStyleSheet(css_not_active)
        self.attendence_button.setStyleSheet(css_not_active)
        self.task_button.setStyleSheet(css_not_active)
        self.setting_button.setStyleSheet(css_not_active)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        self.task_timer = QTimer(self)
        self.task_timer.timeout.connect(self.task_showTime)
        self.task_timer.start(1000)

        self.task_list.itemSelectionChanged.connect(self.selectionChanged)

        self.task_start_button.clicked.connect(self.task_start)
        self.task_stop_button.clicked.connect(self.task_pause)
        self.task_complete_button.clicked.connect(self.task_complete)
        self.add_task_btn.clicked.connect(self.task_add)
        self.refresh_btn.clicked.connect(self.refresh_task)
        self.add_task_btn_2.clicked.connect(self.daily_task)

        self.spinner = QtWaitingSpinner(self)
        # self.spinner.start()
        self.horizontalLayout_4.addWidget(self.spinner)
        # hbox = QHBoxLayout()
        # hbox.addWidget(self.spinner)
        # self.setLayout(hbox)
        self.frame_12.hide()
        # self.Example_Window_task = Example_Window()
        # self.horizontalLayout_4.hide()

    # #########################################################
    def version_btn_fun(self):
        print("version_btn_fun")

    def task(self):

        self.home_button.setStyleSheet(css_not_active)
        self.screen_share.setStyleSheet(css_not_active)
        self.attendence_button.setStyleSheet(css_not_active)
        self.task_button.setStyleSheet(css_active)
        self.setting_button.setStyleSheet(css_not_active)

        # self.Example_Window_task.show()
        self.stackedWidget.setCurrentWidget(self.task_page)

        # try:
        #     self.task_button.setEnabled(False)
        #     print(datetime.datetime.now())
        #     task_url = 'https://www.fineoutput.website/task_manager/employee/api/Home/tasks'
        #     task_list_data = {
        #         'email': self.email,
        #         'password': self.password
        #     }
        #
        #     self.task_r = requests.post(task_url, data=task_list_data)
        #     # print(json.loads(self.task_r.content)['data'])
        #     print("task all details with total_time :",self.task_r.content)
        #     # print(self.task_r)
        #     if json.loads(self.task_r.content)['message'] == 'success':
        #         self.task_button.setEnabled(True)
        #         print(datetime.datetime.now())
        #         # self.Example_Window_task.hide()
        #     self.task_list.clear()
        #     task_list_header = 'ID    Task Name'
        #     self.task_list.addItem(task_list_header)
        #
        #     if json.loads(self.task_r.content)['data'] == "no task":
        #         print("NO TASK")
        #     else:
        #         for i in self.task_r.json()['data']:
        #             print("new task all details :",i['task'])
        #             task_list = i['id'] + "   " + i['task'] + "   " + f"({i['project_name']})" + "   " + f"(" \
        #                                                                                                  f"{i['est_time']})" + "   " + f"({i['time_taken']})"
        #             self.task_list.addItem(task_list)
        # except:
        #     self.task_button.setEnabled(True)
        #     print("Error in task list")
        #     pass
        # ###################################################################

        self.task_start_button.hide()
        self.task_stop_button.hide()
        self.task_complete_button.hide()
        if self.task_time_start:
            self.task_start_button.hide()
            self.task_stop_button.show()
            self.task_complete_button.hide()

    # self.refresh_btn.setEnabled(False)
    def refresh_task(self):
        self.frame_12.show()
        self.spinner.start()
        try:
            self.refresh_btn.setEnabled(False)
            print(datetime.datetime.now())
            task_url = 'https://www.fineoutput.us/employee/api/Home/tasks'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            task_list_data = {
                'email': self.email,
                'password': self.password
            }

            self.task_r = requests.post(task_url, data=task_list_data, headers=headers)
            # print(json.loads(self.task_r.content)['data'])
            print("task all details with total_time :", self.task_r)
            # print(self.task_r)
            if json.loads(self.task_r.content)['message'] == 'success':
                # self.frame_12.hide()
                self.spinner.stop()
                self.refresh_btn.setEnabled(True)
                print(datetime.datetime.now())
                # self.Example_Window_task.hide()
            self.task_list.clear()
            task_list_header = 'ID    Task Name'
            self.task_list.addItem(task_list_header)

            if json.loads(self.task_r.content)['data'] == "no task":
                print("NO TASK")
            else:
                # for idx, val in enumerate(self.task_r.json()['data']):
                #     print(idx, val)
                for i in self.task_r.json()['data']:
                    print("new task all details :", i['task'])
                    task_list = i['id'] + "   " + i['task'] + "   " + f"({i['project_name']})" + "   " + f"(" \
                                                                                                         f"{i['est_time']})" + "   " + f"({i['time_taken']})"
                    self.task_list.addItem(task_list)
        except:
            self.refresh_btn.setEnabled(True)
            print("Error in task list")
            pass

    def daily_task(self):
        self.daily_task_web = Add_task_web()
        self.daily_task_web.setWindowTitle("Daily Task Report")
        self.daily_task_web.setWindowIcon(QtGui.QIcon('logo.png'))
        self.daily_task_web.task_browser.setUrl(QUrl('https://www.fineoutput.us/employee/bhadmin/Daily_report/view_dailyreport'))

        self.daily_task_web.show()

    def task_add(self):
        print("add task btn click")
        # self.add_task_dialog = Add_task()
        self.Add_task_web = Add_task_web()

        # self.add_task_dialog.setWindowTitle("Create Task")
        # self.add_task_dialog.setWindowIcon(QtGui.QIcon('logo.png'))
        # self.add_task_dialog.show()

        self.Add_task_web.setWindowTitle("Create Task")
        self.Add_task_web.setWindowIcon(QtGui.QIcon('logo.png'))
        self.Add_task_web.task_browser.setUrl(QUrl('https://www.fineoutput.us/employee/bhadmin/tasks/view_tasks2'))

        self.Add_task_web.show()

        # ############################
        # try:
        #     project_list_url = "https://www.fineoutput.website/task_manager/employee/api/Home/projects_list"
        #
        #     project_list_data = {
        #         'email': self.email,
        #         'password': self.password
        #     }
        #
        #     self.project_list_response = requests.post(project_list_url, data=project_list_data)
        #     self.project_list_response = json.loads(self.project_list_response.content)
        #     print(self.project_list_response['data'])
        #
        #     project_list = self.project_list_response['data']
        #     project_dropdown = []
        #     for project in project_list:
        #         project_dropdown.append(project['project_name'])
        #     self.add_task_dialog.comboBox.setEditable(True)
        #     self.add_task_dialog.comboBox.addItems(project_dropdown)
        #
        #     task_type = ['New', 'Error']
        #     self.add_task_dialog.comboBox_2.addItems(task_type)
        #     # self.add_task_dialog.comboBox_2.addItems()
        # except:
        #     print("task_add except")
        # self.add_task_dialog.pushButton.clicked.connect(self.task_add_get)

    # def task_add_get(self):
    #     self.add_task_dialog.lineEdit.text()
    #     # self.add_task_dialog.lineEdit_2.text()
    #     cre_task_time = self.add_task_dialog.dateTimeEdit.dateTime()
    #     print(type(cre_task_time))
    #     cre_task_time = str(cre_task_time)
    #     cre_task_time = cre_task_time[23:-1]
    #     cre_task_time = cre_task_time.split(',')
    #     cre_task_time = cre_task_time[0].strip()+"-"+cre_task_time[1].strip()+"-"+cre_task_time[2].strip(
    #
    #     )+" "+cre_task_time[
    #         3].strip()+":"+cre_task_time[4].strip()+":"+"00"
    #     print(cre_task_time)
    #     self.add_task_dialog.comboBox.currentText()
    #     self.add_task_dialog.comboBox_2.currentText()
    #     if self.add_task_dialog.comboBox_2.currentText() == 'New':
    #         self.task_type = 1
    #     elif self.add_task_dialog.comboBox_2.currentText() == 'Error':
    #         self.task_type = 2
    #     else:
    #         pass
    #
    #     try:
    #         for project_name in self.project_list_response['data']:
    #             if self.add_task_dialog.comboBox.currentText() == project_name['project_name']:
    #                 project_id_send_for_create_task = project_name['project_id']
    #                 print("project id or name matched", project_id_send_for_create_task)
    #     except:
    #         pass
    #     try:
    #         create_task_url = "https://www.fineoutput.us/employee/api/Home/create_task"
    #
    #         create_task_data = {
    #             'email': self.email,
    #             'password': self.password,
    #             'task': self.add_task_dialog.lineEdit.text(),
    #             'est_time': cre_task_time,
    #             'project_id': project_id_send_for_create_task,
    #             'task_type': self.task_type
    #         }
    #         add_task_response = requests.post(create_task_url, data=create_task_data)
    #         print("add task responce for succecc",json.loads(add_task_response.content))
    #         # print(add_task_response.content)
    #
    #         print(self.add_task_dialog.lineEdit.text(), self.add_task_dialog.lineEdit_2.text(),
    #               self.add_task_dialog.comboBox.currentText())
    #     except:
    #         print("task_add get except")
    #
    #     try:
    #         if add_task_response.status_code == 200:
    #
    #             success_msg = json.loads(add_task_response.content)
    #             success_msg = success_msg['data']
    #             print("success_msg",success_msg.title())
    #             self.succ_task_create = task_create_dialog()
    #             self.succ_task_create.label.setText(success_msg.title())
    #             self.succ_task_create.label.setAlignment(QtCore.Qt.AlignCenter)
    #             # self.version_button.clicked.connect(self.version_btn_fun)
    #             self.succ_task_create.task_cre_succ_btn.clicked.connect(self.tsk_cre_succ_bttn)
    #             self.add_task_dialog.hide()
    #             task_url = 'https://www.fineoutput.us/employee/api/Home/tasks'
    #             task_list_data = {
    #                 'email': self.email,
    #                 'password': self.password
    #             }
    #
    #             self.task_r = requests.post(task_url, data=task_list_data)
    #             if self.task_r.status_code == 200:
    #                 # self.succ_task_create.hide()
    #                 pass
    #             # print(json.loads(self.task_r.content)['data'])
    #             # print(self.task_r.content)
    #             # print(self.task_r)
    #             self.task_list.clear()
    #             task_list_header = 'ID    Task Name'
    #             self.task_list.addItem(task_list_header)
    #
    #             if json.loads(self.task_r.content)['data'] == "no task":
    #                 print("NO TASK")
    #             else:
    #                 for i in self.task_r.json()['data']:
    #                     # print(i['task'])
    #                     task_list = i['id'] + "   " + i['task'] + "   " + f"({i['project_name']})" + "   " + f"(" \
    #                                                                                                          f"{i['est_time']})" + "   " + f"({i['time_taken']})"
    #                     self.task_list.addItem(task_list)
    #     except:
    #         # self.succ_task_create = task_create_dialog('create succfully')
    #         # time.sleep(3)
    #         self.add_task_dialog.hide()
    #         print("error in fetch task")
    #         pass

    def tsk_cre_succ_bttn(self):
        self.succ_task_create.hide()
        print("tsk_cre_succ_bttn ok click")

    def task_start(self):
        self.frame_12.show()
        self.spinner.start()
        print("Task Start Button clicked")
        self.task_select_flag = True
        self.task_time_start = True
        self.task_start_button.hide()
        self.task_stop_button.show()
        self.task_complete_button.hide()

        for_loop_break_flag = False
        key = self.task_name[0]

        # //////////////////////////////////
        # #########################################

        # print("self.task_name[0] :: ",key)
        # if key in self.task_name_total_time_dist.keys():
        #     # ////////////////////
        #     if self.task_Keyloger.stop_threads == False:
        #         print("keylogger thread false")
        #         keyloger_task_flag = 'TASK'
        #         self.task_Keyloger = Keyloger(keyloger_task_flag)
        #         self.task_Keyloger.start()
        #         # self.task_Keyloger.stop_threads = True
        #     else:
        #         print("keylogger thread true")
        #     # ///////////////////
        #     print("task_ start if block")
        #     self.total_task_time = 0
        #     for t in self.task_name_total_time_dist[key]:
        #         self.total_task_time += int(t)
        #
        #     # ###############################
        #
        #     task_seconds = self.total_task_time % (24 * 3600)
        #     task_hour = task_seconds // 3600
        #     task_seconds %= 3600
        #     task_minutes = task_seconds // 60
        #     task_seconds %= 60
        #
        #     if len(str(task_hour)) > 1:
        #         task_hour = str(task_hour)
        #     else:
        #         task_hour = '0' + str(task_hour)
        #
        #     if len(str(task_minutes)) > 1:
        #         task_minutes = str(task_minutes)
        #     else:
        #         task_minutes = '0' + str(task_minutes)
        #
        #     if len(str(task_seconds)) > 1:
        #         task_seconds = str(task_seconds)
        #     else:
        #         task_seconds = '0' + str(task_seconds)
        #
        #     # self.task_time_taken =
        #     # ###############################
        #     total_task_time = f'Total Time : {task_hour}:{task_minutes}:{task_seconds}'
        #
        #     self.task_total_time_label.setText(total_task_time)
        #
        #     # self.task_Keyloger = Keyloger()
        #     # self.task_Keyloger.start()
        #     # self.task_name_total_time_dist[key].append(lst)
        # else:
        print("task_ start else block")
        for data in self.task_r.json()['data']:
            for nm in data.keys():
                if data[nm] == key:
                    print("first for loop break")
                    self.total_task_time = 'Total Time : 00:00:00'
                    for_loop_break_flag = True
                    break
                else:
                    self.total_task_time = 'Total Time : 00:00:00'
            if for_loop_break_flag:
                print("secound for loop")
                for_loop_break_flag = False
                break
            else:
                pass
        keyloger_task_flag = 'TASK'
        self.task_Keyloger = Keyloger(keyloger_task_flag)
        self.task_Keyloger.start()
        self.task_total_time_label.setText(self.total_task_time)
        # #########################################
        print("task name for secound api :: email pass ", self.email, self.password)
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            task_time_url = "https://www.fineoutput.us/employee/api/Home/start_data"
            self.task_id = self.task_name[0]
            data_for_time = {'task_id': self.task_id,
                             'email': self.email,
                             'password': self.password
                             }
            start_task_response = requests.post(task_time_url, data=data_for_time, headers=headers)
            print(start_task_response)

            start_task_response = json.loads(start_task_response.content)
            print(start_task_response)
            print("task detail id: ",start_task_response['task_detail_id'])
            self.task_detail_id = start_task_response['task_detail_id']
        except:
            print("task_start except first")
        #     ////////////////////////////////////
        task_detail_data = {'task_id': self.task_id,
                            'email': self.email,
                            'password': self.password,

                            }

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            task_detail_url = "https://www.fineoutput.us/employee/api/Home/task_details"
            task_detail_responce = requests.post(task_detail_url, data=task_detail_data, headers=headers)
            # print("task detail response",task_detail_responce)
            if task_detail_responce.status_code == 200:
                # self.frame_12.hide()
                self.spinner.stop()
                print("ok")
            task_detail_responce = json.loads(task_detail_responce.content)
            print("task detail response content 111111111111111111 :", task_detail_responce['data'])
            self.task_work_detailed_list.clear()
            header_for_task_details = 'Start Time                     End Time'
            self.task_work_detailed_list.addItem(header_for_task_details)

            for task in task_detail_responce['data']:
                print("Task detail ::: ", task)
                task_details_add_in_list = f'{task["start_time"]}     {task["end_time"]}'
                self.task_work_detailed_list.addItem(task_details_add_in_list)
        except:
            print("task_start except secound")
        print("start btn fun complete")

    # ///////////////////////////////////////

    def task_pause(self):

        self.frame_12.show()
        self.spinner.start()

        self.task_select_flag = False
        self.task_time_start = False
        self.task_start_button.show()
        self.task_stop_button.hide()
        self.task_complete_button.show()
        self.task_Keyloger.stop_threads = False
        print("task keyloger keys ::: ", self.task_Keyloger.Task_keyloger_multi_string)

        key = self.task_name[0]
        if key in self.task_name_total_time_dist.keys():
            print("task_pause if block")

            lst = self.task_time_count
            self.task_name_total_time_dist[key].append(lst)
        else:
            print("task_pause else block")
            self.task_name_total_time_dist[key] = []

            lst = self.task_time_count
            print("lst :", lst)
            self.task_name_total_time_dist[key].append(lst)

        print("Not present", self.task_name_total_time_dist)
        # ##########################################################

        if key in self.task_name_total_time_dist.keys():
            self.total_task_time = 0
            for t in self.task_name_total_time_dist[key]:
                self.total_task_time += int(t)
            total_task_seconds = self.total_task_time % (24 * 3600)
            total_task_hour = total_task_seconds // 3600
            total_task_seconds %= 3600
            total_task_minutes = total_task_seconds // 60
            total_task_seconds %= 60

            if len(str(total_task_hour)) > 1:
                total_task_hour = str(total_task_hour)
            else:
                total_task_hour = '0' + str(total_task_hour)

            if len(str(total_task_minutes)) > 1:
                total_task_minutes = str(total_task_minutes)
            else:
                total_task_minutes = '0' + str(total_task_minutes)

            if len(str(total_task_seconds)) > 1:
                total_task_seconds = str(total_task_seconds)
            else:
                total_task_seconds = '0' + str(total_task_seconds)

            # self.task_time_taken =
            # ###############################
            self.total_task_time_string = f'{total_task_hour}:{total_task_minutes}:{total_task_seconds}'
            total_task_time = f'Total Time : {total_task_hour}:{total_task_minutes}:{total_task_seconds}'

            self.task_total_time_label.setText(total_task_time)
            print("total000000 : ", self.total_task_time_string)
        # ##########################################################
        task_seconds = self.task_time_count % (24 * 3600)
        task_hour = task_seconds // 3600
        task_seconds %= 3600
        task_minutes = task_seconds // 60
        task_seconds %= 60

        if len(str(task_hour)) > 1:
            task_hour = str(task_hour)
        else:
            task_hour = '0' + str(task_hour)

        if len(str(task_minutes)) > 1:
            task_minutes = str(task_minutes)
        else:
            task_minutes = '0' + str(task_minutes)

        if len(str(task_seconds)) > 1:
            task_seconds = str(task_seconds)
        else:
            task_seconds = '0' + str(task_seconds)

        self.task_time_taken = f'{task_hour}:{task_minutes}:{task_seconds}'

        task_list = f"{self.task_name[1]} ({self.task_time_taken})"
        # self.task_work_detailed_list.addItem(task_list)
        # //////////////Task Detail//////////////////

        # ///////////////////////////////////////////
        # self.task_total_time_label.setText(self.total_task_time)
        # print("task taken time : ", self.task_time_taken)
        self.task_time_count = 0
        # ////////////////////////////////////////

        self.task_id = self.task_name[0]
        # print("Waste time list : ", self.wasted_time)
        if len(self.wasted_time) == 0:
            self.waste_time_send = '00:00:00'

        else:
            self.waste_time = 0
            for waste_time in self.wasted_time:
                self.waste_time = self.waste_time + waste_time
            # print("waste_time :: ", self.change_time_form(self.waste_time))
            self.waste_time_send = self.change_time_form(self.waste_time)

        data_for_time = {'task_id': self.task_id,
                         'email': self.email,
                         'password': self.password,
                         'task_detail_id': self.task_detail_id,
                         'total_time': self.task_time_taken,
                         'wasted_time': self.waste_time_send,
                         }
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            task_time_url = "https://www.fineoutput.us/employee/api/Home/stop_data"
            r = requests.post(task_time_url, data=data_for_time,headers=headers)
            print(r)
            print(r.content)


        #     /////////////////////task detail update when stop///////////////////
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            task_detail_data = {'task_id': self.task_id,
                                'email': self.email,
                                'password': self.password,

                                }
            task_detail_url = "https://www.fineoutput.us/employee/api/Home/task_details"
            task_detail_responce = requests.post(task_detail_url, data=task_detail_data, headers=headers)
            if task_detail_responce.status_code == 200:
                print("hulle hulla")
                # ///////////////////////////////////////////////////////////////////////////
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                task_url = 'https://www.fineoutput.us/employee/api/Home/tasks'
                task_list_data = {
                    'email': self.email,
                    'password': self.password
                }

                self.task_r = requests.post(task_url, data=task_list_data,headers=headers)
                if self.task_r.status_code == 200:
                    print('ok')
                    # self.frame_12.hide()
                    self.spinner.stop()
                self.task_list.clear()
                task_list_header = 'ID    Task Name'
                self.task_list.addItem(task_list_header)

                if json.loads(self.task_r.content)['data'] == "no task":
                    print("NO TASK")
                else:
                    for i in self.task_r.json()['data']:
                        task_list = i['id'] + "   " + i['task'] + "   " + f"({i['project_name']})" + "   " + f"(" \
                                                                                                             f"{i['est_time']})" + "   " + f"({i['time_taken']})"
                        self.task_list.addItem(task_list)
            # /////////////////////////////////////////////////////////////////////
                # print("task detail response",task_detail_responce)
                task_detail_responce = json.loads(task_detail_responce.content)
                print("task detail response content 111111111111111111 :", task_detail_responce['data'])
                self.task_work_detailed_list.clear()
                header_for_task_details = 'Start Time                     End Time'
                self.task_work_detailed_list.addItem(header_for_task_details)

                for task in task_detail_responce['data']:
                    print("Task detail ::: ", task)
                    task_details_add_in_list = f'{task["start_time"]}     {task["end_time"]}'
                    self.task_work_detailed_list.addItem(task_details_add_in_list)

        #     ////////////////////////////////////////////////////////////////////
        except:
            print("task_stop except ")

    def complete_task_responce_ok_btn(self):
        self.frame_12.show()
        self.spinner.start()
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            task_url = 'https://www.fineoutput.us/employee/api/Home/tasks'
            task_list_data = {
                        'email': self.email,
                        'password': self.password
                    }

            self.task_r = requests.post(task_url, data=task_list_data,headers=headers)
            if self.task_r.status_code == 200:
                print("ok")
                # self.frame_12.hide()
                self.spinner.stop()
            self.task_list.clear()
            task_list_header = 'ID    Task Name'
            self.task_list.addItem(task_list_header)

            if json.loads(self.task_r.content)['data'] == "no task":
                print("NO TASK")
            else:
                for i in self.task_r.json()['data']:
                    task_list = i['id'] + "   " + i['task'] + "   " + f"({i['project_name']})" + "   " + f"(" \
                                                                                                         f"{i['est_time']})" + "   " + f"({i['time_taken']})"
                    self.task_list.addItem(task_list)
            self.task_complete_dialog_after_responce.hide()
        except:
            print("complete_task_responce_ok_btn except block")

    def task_complete_ok_btn(self):
        self.frame_12.show()
        self.spinner.start()
        self.task_complete_dialog.hide()
        print("task_complete_ok_btn")

        self.task_complete_flag = True
        self.task_select_flag = False
        self.task_time_start = False
        self.task_start_button.hide()
        self.task_stop_button.hide()
        self.task_complete_button.hide()

        keyloger_com_task_flag = 'Attendence'
        self.task_com_Keyloger = Keyloger(keyloger_com_task_flag)
        self.task_com_Keyloger.start()

        if len(self.wasted_time) == 0:
            self.waste_time_send = '00:00:00'

        else:

            for waste_time in self.wasted_time:
                self.waste_time = self.waste_time + waste_time
            print("waste_time :: ", self.change_time_form(self.waste_time))
            self.waste_time_send = self.change_time_form(self.waste_time)
        data_for_task_complete = {'task_id': self.task_id,
                                  'email': self.email,
                                  'password': self.password,
                                  'task_detail': self.task_detail_id,
                                  'total_time': self.task_time_taken,
                                  'wasted_time': self.waste_time_send,
                                  'keylogger': self.task_Keyloger.Task_keyloger_multi_string}
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

            task_Complete_url = 'https://www.fineoutput.us/employee/api/Home/task_complete'
            r = requests.post(task_Complete_url, data=data_for_task_complete, headers=headers)
            print("COMPLETE TASK",r)
            resp = json.loads(r.content)
            print("COMPLETE TASK", resp)
            if r.status_code == 200:
                print("ok")
                # self.frame_12.hide()
                self.spinner.stop()
                self.task_complete_dialog_after_responce = task_complete_dialog_after_responce()
                succ_mess = resp['message'].title()
                self.task_complete_dialog_after_responce.label.setText(succ_mess)
                self.task_complete_dialog_after_responce.label.setAlignment(QtCore.Qt.AlignCenter)
                self.task_complete_dialog_after_responce.pushButton.clicked.connect(
                    self.complete_task_responce_ok_btn)

            # if r.status_code == 200:
            #     task_detail_data = {'task_id': self.task_id,
            #                         'email': self.email,
            #                         'password': self.password,
            #
            #                         }
            #
            #     task_detail_url = "https://www.fineoutput.website/task_manager/employee/api/Home/task_details"
            #     task_detail_responce = requests.post(task_detail_url, data=task_detail_data)
            #     if task_detail_responce.status_code == 200:
            #         print("hulle hulla")
            #         # ///////////////////////////////////////////////////////////////////////////
            #         task_url = 'https://www.fineoutput.website/task_manager/employee/api/Home/tasks'
            #         task_list_data = {
            #             'email': self.email,
            #             'password': self.password
            #         }
            #
            #         self.task_r = requests.post(task_url, data=task_list_data)
            #         self.task_list.clear()
            #         task_list_header = 'ID    Task Name'
            #         self.task_list.addItem(task_list_header)
            #
            #         if json.loads(self.task_r.content)['data'] == "no task":
            #             print("NO TASK")
            #         else:
            #             for i in self.task_r.json()['data']:
            #                 task_list = i['id'] + "   " + i['task'] + "   " + f"({i['project_name']})" + "   " + f"(" \
            #                                                                                                      f"{i['est_time']})" + "   " + f"({i['time_taken']})"
            #                 self.task_list.addItem(task_list)
            #     # /////////////////////////////////////////////////////////////////////
            #     # print("task detail response",task_detail_responce)
            #     task_detail_responce = json.loads(task_detail_responce.content)
            #     print("task detail response content 111111111111111111 :", task_detail_responce['data'])
            #     self.task_work_detailed_list.clear()
            #     header_for_task_details = 'Start Time                     End Time'
            #     self.task_work_detailed_list.addItem(header_for_task_details)
            #
            #     for task in task_detail_responce['data']:
            #         print("Task detail ::: ", task)
            #         task_details_add_in_list = f'{task["start_time"]}     {task["end_time"]}'
            #         self.task_work_detailed_list.addItem(task_details_add_in_list)


        except:
            print("task_complete EXCEPT ")
            print("start btn fun complete")

    def task_complete_cancel_btn(self):
        self.task_complete_dialog.hide()

    def task_complete(self):
        # ////////////////////////////
        self.task_complete_dialog = task_complete_dialog()
        self.task_complete_dialog.label.setText("Do You Want To Complete Task.")
        self.task_complete_dialog.label.setAlignment(QtCore.Qt.AlignCenter)
        self.task_complete_dialog.pushButton.clicked.connect(self.task_complete_ok_btn)
        self.task_complete_dialog.pushButton_2.clicked.connect(self.task_complete_cancel_btn)
        # ////////////////////////////


    def task_showTime(self):
        try:
            if self.task_time_start:
                # print("self.Keyloger.write_time :: ", self.task_Keyloger.write_time)
                task_cur_x = datetime.datetime.now()
                task_cur_x = int(task_cur_x.strftime("%H") + "" + task_cur_x.strftime("%M") + "" + task_cur_x.strftime(
                    "%S"))
                # print("cur_x for task showtime", task_cur_x)
            else:
                pass
                # print("try else block")
        except:
            pass
            # print("self.Keyloger.write_time")
        if self.task_time_start:
            self.task_time_count += 1

        if self.task_complete_flag:
            self.text = f'Task Complete..!!'
            self.task_time_label.setText(self.text)

        # /////////task time cut when employee does not type /////////
        try:
            if self.task_time_start:
                if (int(self.task_Keyloger.write_time) - int(task_cur_x)) != 0:
                    task_cur_x = str(task_cur_x)
                    task_cur_x = task_cur_x[-2:]
                    # print("last two dogit of time", task_cur_x)
                    task_keyloger_write_time = str(self.task_Keyloger.write_time)
                    task_keyloger_write_time = task_keyloger_write_time[-2:]

                    if ((int(task_keyloger_write_time) == int(task_cur_x))):
                        print("time same")
                        self.task_time_count = self.task_time_count - 60
                        self.wasted_time.append(60)
                else:
                    pass
            else:
                # print("san")
                pass
        except:
            print("time cut except block")
        # ////////////////////////////////////////////////////////////
        if self.task_time_start:

            text = self.task_time_count
            task_seconds = text % (24 * 3600)
            task_hour = task_seconds // 3600
            task_seconds %= 3600
            task_minutes = task_seconds // 60
            task_seconds %= 60

            if len(str(task_hour)) > 1:
                task_hour = str(task_hour)
            else:
                task_hour = '0' + str(task_hour)

            if len(str(task_minutes)) > 1:
                task_minutes = str(task_minutes)
            else:
                task_minutes = '0' + str(task_minutes)

            if len(str(task_seconds)) > 1:
                task_seconds = str(task_seconds)
            else:
                task_seconds = '0' + str(task_seconds)

            self.text = f'Time : {task_hour}:{task_minutes}:{task_seconds}'
            self.task_time_label.setText(self.text)

    def selectionChanged(self):
        try:
            self.task_list.setItemSelected(False)
        except:
            print("selectionChanged function")
        if self.task_select_flag == False:

            # self.Example_Window_task.show()
            self.frame_12.show()
            self.spinner.start()

            self.task_complete_flag = False

            self.task = 'Task Name : '
            self.name = self.task_list.currentItem().text()
            print("Task Name :: ",self.name)
            self.task_name = self.name.split("   ")
            print("552332", self.task_name)

            self.full_task_name = self.task + self.task_name[1]

            self.task_name_label.setText(self.full_task_name)
            self.task_time_label.setText("Time : 00:00:00")
            self.task_total_time_label.setText("Total Time : 00:00:00")

            if self.task_name[0] == 'ID':
                print('ID selected')
                self.task_start_button.hide()
            else:
                self.task_start_button.show()

        #     /////////////////////TASK SELECT WHEN UPDATE TASK DETAIL LIST////////////////////////////
            task_detail_data = {'task_id': self.task_name[0],
                                'email': self.email,
                                'password': self.password,

                                }
            task_detail_url = "https://www.fineoutput.us/employee/api/Home/task_details"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

            # /////////////////////////////////////////////////////////////////////
            # print("task detail response",task_detail_responce)
            try:
                # self.cir_loding = Loading()
                task_detail_responce = requests.post(task_detail_url, data=task_detail_data,headers=headers)
                if task_detail_responce.status_code == 200:
                    # self.frame_12.hide()
                    self.spinner.stop()
                    print("request complete")
                    # self.Example_Window_task.hide()
                task_detail_responce = json.loads(task_detail_responce.content)
                print("task detail response content 111111111111111111 :", task_detail_responce['data'])
                self.task_work_detailed_list.clear()
                header_for_task_details = 'Start Time                     End Time'
                self.task_work_detailed_list.addItem(header_for_task_details)
                for task in task_detail_responce['data']:
                    print("Task detail ::: ", task)
                    task_details_add_in_list = f'{task["start_time"]}     {task["end_time"]}'
                    self.task_work_detailed_list.addItem(task_details_add_in_list)
            except:
                self.task_work_detailed_list.clear()
                header_for_task_details = 'Start Time                     End Time'
                self.task_work_detailed_list.addItem(header_for_task_details)

                print("task selected show details")
        # ////////////////////////////////////////////////////////////////////////////////////
        else:
            print("Task Already Selected ...!!")

    def change_time_form(self, sec):
        task_seconds = sec % (24 * 3600)
        task_hour = task_seconds // 3600
        task_seconds %= 3600
        task_minutes = task_seconds // 60
        task_seconds %= 60

        if len(str(task_hour)) > 1:
            task_hour = str(task_hour)
        else:
            task_hour = '0' + str(task_hour)

        if len(str(task_minutes)) > 1:
            task_minutes = str(task_minutes)
        else:
            task_minutes = '0' + str(task_minutes)

        if len(str(task_seconds)) > 1:
            task_seconds = str(task_seconds)
        else:
            task_seconds = '0' + str(task_seconds)

        return f'{task_hour}:{task_minutes}:{task_seconds}'

        # task_list = f"{self.task_name[1]} ({self.task_time_taken})"

    def home(self):
        self.browse_window.setUrl(QUrl(self.url))
        print("home for list selection checking")
        # self.task_list.setItemSelected(item, False)
        print("hodkdsk")
        self.home_button.setStyleSheet(css_active)
        self.screen_share.setStyleSheet(css_not_active)
        self.attendence_button.setStyleSheet(css_not_active)
        self.task_button.setStyleSheet(css_not_active)
        self.setting_button.setStyleSheet(css_not_active)

        print("home page 1")
        self.stackedWidget.setCurrentWidget(self.home_page)

    def screenshare(self):
        self.home_button.setStyleSheet(css_not_active)
        self.screen_share.setStyleSheet(css_active)
        self.attendence_button.setStyleSheet(css_not_active)
        self.task_button.setStyleSheet(css_not_active)
        self.setting_button.setStyleSheet(css_not_active)

        # //////image show label///////

        # //////////////////////////////

        self.ip_dialog = IpDialog()
        self.ip_dialog.setWindowTitle("Scan Ip")
        self.ip_dialog.setWindowIcon(QtGui.QIcon('logo.png'))
        self.ip_dialog.show()
        self.ip_dialog.ip_ok_btn.clicked.connect(self.ok)
        self.ip_dialog.scan_ip_btn.clicked.connect(self.scan_ips)

        self.ip_dialog.ip_list_view.itemSelectionChanged.connect(self.selected_ip)

        if self.client_thread_counter == 0:
            self.client_thread_counter = self.client_thread_counter + 1
            if self.client_thread_stop == False:
                self.thread_client.start()
                self.video_share_thread_stop = False
        else:
            self.client_thread_counter = self.client_thread_counter + 1
            print("self.client_thread_counter ::: ", self.client_thread_counter)

        # self.thread_client.start()

        # self.count = self.count+1
        # self.i = self.i+1
        # self.stackedWidget.setCurrentWidget(self.accounts_page)
        # print(f"counting of screen share button click :: {self.i}")
        # if self.count == 2:
        #     if self.video_share_thread_stop ==False:
        #         # self.port = 12312
        #         print("server_ip_video_thread_flag ????? ",server_ip_video_thread_flag)
        #         if server_ip_video_thread_flag == False:
        #             print("server_ip_video selected if ", )
        #
        #         # print("VideoThread start port at :".upper(),self)
        #         try:
        #             self.screen_share_ip = self.selected_item_ip_list
        #             print("screen share ip &&&&&&&& ",self.screen_share_ip)
        #         except:
        #             print("screen share ip &&&&&&&& ERROR !!!!!!")
        #
        #         self.thread = VideoThread(self.video_thread_port)
        #         self.thread.change_pixmap_signal.connect(self.update_image)
        #         self.thread.start()
        #         # self.port = self.port +1

    def screen_share_thread(self, ip_name):
        print("IP NAME : ", ip_name)
        self.ip_name = ip_name
        self.count = self.count + 1
        self.i = self.i + 1
        self.stackedWidget.setCurrentWidget(self.accounts_page)
        print(f"counting of screen share button click :: {self.i}")
        if self.count == 2:
            if self.video_share_thread_stop == False:
                # self.port = 12312
                print("server_ip_video_thread_flag ????? ", server_ip_video_thread_flag)
                if server_ip_video_thread_flag == False:
                    print("server_ip_video selected if ", )

                # print("VideoThread start port at :".upper(),self)
                try:
                    self.screen_share_ip = self.selected_item_ip_list
                    print("screen share ip &&&&&&&& ", self.screen_share_ip)
                except:
                    print("screen share ip &&&&&&&& ERROR !!!!!!")

                self.thread = VideoThread(self.video_thread_port, self.ip_name)
                self.thread.change_pixmap_signal.connect(self.update_image)
                self.thread.start()
                # self.port = self.port +1

    def selected_ip(self):
        self.selected_item_ip_list = self.ip_dialog.ip_list_view.currentItem().text()
        # print("selected ip :::: ", self.selected_item_ip_list)

    def scan_ips(self):
        print("scan ips :: ")
        self.ip_list = get_ips()
        self.ip_dialog.ip_list_view.clear()
        header_for_ip = "IP                 Mac Address"

        self.ip_dialog.ip_list_view.addItem(header_for_ip)
        for ip in self.ip_list:
            ip_list = ip['ip'] + "   " + ip['mac']
            print("ip_list:::", ip_list)
            self.ip_dialog.ip_list_view.addItem(ip_list)
        print("scan ips funished:: ")

    def ok(self):
        if self.selected_item_ip_list:
            # print("selected ip :::: ok button ", self.selected_item_ip_list)
            self.selected_item_ip_list = self.selected_item_ip_list.split("   ")
            print("selected ip :::: ok button ", self.selected_item_ip_list)
            self.selected_item_ip_list = self.selected_item_ip_list[0]
            self.ip_dialog.hide()
            self.screen_share_thread(self.selected_item_ip_list)
        else:
            print("please select ip")

    def attendence(self):
        self.home_button.setStyleSheet(css_not_active)
        self.screen_share.setStyleSheet(css_not_active)
        self.attendence_button.setStyleSheet(css_active)
        self.task_button.setStyleSheet(css_not_active)
        self.setting_button.setStyleSheet(css_not_active)

        print("self.lunch_break_button_handle attendence block".upper(), self.lunch_break_button_handle)
        if self.lunch_break_button_handle == 'pause':
            # print("jhsdjhdshjkfdhjkfdhkjfdshjfds")
            self.resume_button.show()
            self.pause_button.hide()

        elif self.lunch_break_button_handle == 'resume':
            self.resume_button.hide()
            self.pause_button.show()
        else:
            self.resume_button.hide()
            self.pause_button.show()
        if self.start_button_flag:
            print("1")
            # self.resume_button.hide()
            # self.pause_button.show()

            self.stackedWidget.setCurrentWidget(self.attendence_page)
        elif self.start_button_flag == '':
            print("2")
            self.stackedWidget.setCurrentWidget(self.settings_page)
            self.start_button.clicked.connect(self.start)
        else:
            print("attendence Start Page 3".upper())

            self.stackedWidget.setCurrentWidget(self.settings_page)
            self.start_button.clicked.connect(self.start)

    def attendence_start_ok_btn_response(self):
        self.attendence_start_dialog_responce_message.hide()

    def attendence_start_ok_btn(self):
        self.attendence_start_dialog.hide()
        print("attendence_start_ok_btn")

        try:

            URL = "https://www.fineoutput.us/employee/api/Home/attendance"

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            r = requests.post(url=URL, data={'email': self.email, 'password': self.password}, headers=headers)
            # r = requests.post(url=URL, data={'email': self.email, 'password': self.password})
            print("###############", r)
            print("responce :: ", r.text)
            res = json.loads(r.text)
            # ??????????????????After attendence start ?????????????????????
            if r.status_code == 200:
                self.attendence_start_dialog_responce_message = attendence_start_dialog_responce_message()
                # self.attendence_start_dialog_responce_message.
                succ_mess = res['message'].title()
                self.attendence_start_dialog_responce_message.label.setText(succ_mess)
                self.attendence_start_dialog_responce_message.label.setAlignment(QtCore.Qt.AlignCenter)
                self.attendence_start_dialog_responce_message.pushButton.clicked.connect(self.attendence_start_ok_btn_response)

            # ??????????????????????????

            # res = r.text
            print(res['data'])
            if res['data'] == '':
                self.string_time = 'Time : 0:0:0'
            elif res['data'] == '"00:00:00"':
                self.string_time = 'Time : 0:0:0'
            else:

                self.string_time = str(res['data'])

                # ////////////////////////////////////////////////////////////////////////////////////////////

                time_set_after_read_database1 = self.string_time
                print("time_set_after_read_database1", time_set_after_read_database1)
                time_set_after_read_database1 = time_set_after_read_database1.split(":")
                print(" ::: time_set_after_read_database ::: ", time_set_after_read_database1)
                if time_set_after_read_database1[0] != ' 00':
                    print("h",time_set_after_read_database1[0])
                    hour_in_sec = int(time_set_after_read_database1[0]) * 60 * 60

                else:
                    print("he",time_set_after_read_database1[0])
                    hour_in_sec = int(time_set_after_read_database1[0]) * 60 * 60

                if time_set_after_read_database1[1] != '00':
                    print("m",time_set_after_read_database1[1])
                    minute_in_sec = int(time_set_after_read_database1[1]) * 60
                else:
                    print("me",time_set_after_read_database1[1])
                    minute_in_sec = int(time_set_after_read_database1[1]) * 60

                if time_set_after_read_database1[2] != '00':
                    print("s",time_set_after_read_database1[2])
                    second_in_sec = int(time_set_after_read_database1[2])

                else:
                    print("se",time_set_after_read_database1[2])
                    second_in_sec = int(time_set_after_read_database1[2])

                self.time_count = hour_in_sec + minute_in_sec + second_in_sec

            self.time_label.setText(self.string_time)
            self.time_start = True
            self.web_block_flag = True
        except:
            print("attendence_start except ")

        keyloger_task_flag = 'Attendence'
        self.Keyloger = Keyloger(keyloger_task_flag)
        self.Keyloger.start()

        self.stackedWidget.setCurrentWidget(self.attendence_page)
        if self.web_block_flag == True:
            web_block_thread = threading.Thread(target=self.website_block)
            web_block_thread.start()
        print("self.lunch_break_button_handle start block".upper(), self.lunch_break_button_handle)
        # if self.lunch_break_button_handle == '':
        #     self.resume_button.hide()
        #     self.pause_button.show()
        # elif self.lunch_break_button_handle == 'resume':
        #     self.resume_button.show()
        #     self.pause_button.hide()
        # elif self.lunch_break_button_handle == 'pause':
        #     self.resume_button.hide()
        #     self.pause_button.show()
        self.pause_button.clicked.connect(self.pause)
        self.resume_button.clicked.connect(self.resume)
        self.stop_button.clicked.connect(self.stop)

    def attendence_start_cancel_btn(self):
        self.attendence_start_dialog.hide()
        print("attendence_start_cancel_btn")

    def start(self):
        print("start button click", self.email, self.password)
        # ////////////////////////////////////////////////////////
        # attendence_start_dialog
        self.attendence_start_dialog = attendence_start_dialog()
        self.attendence_start_dialog.label.setText("Attendance Start !! ")
        self.attendence_start_dialog.label.setAlignment(QtCore.Qt.AlignCenter)
        self.attendence_start_dialog.pushButton.clicked.connect(self.attendence_start_ok_btn)
        self.attendence_start_dialog.pushButton_2.clicked.connect(self.attendence_start_cancel_btn)
        # ////////////////////////////////////////////////////////
        self.start_button_flag = True
        # ##############KEYLOGGER REQUEST#################

        # URL = "http://localhost/customci3.1/Api/attendance"


    # ##########################################################

    def website_block(self):
        hostsPath = "C:\Windows\System32\drivers\etc\hosts"
        # redirect = "192.168.0.101"
        host_name = socket.gethostname()
        redirect = socket.gethostbyname(host_name)
        websites = ["www.facebook.com", "facebook.com", ]
        while True:
            # Duration during which, website blocker will work
            if dt(dt.now().year, dt.now().month, dt.now().day, 9) < dt.now() < dt(dt.now().year, dt.now().month,
                                                                                  dt.now().day, 18):
                # print("Sorry Not Allowed...")
                if self.web_block:
                    break
                try:
                    with open(hostsPath, 'r+') as file:
                        # print("with block")
                        content = file.read()
                        # print('#' * 50)
                        # print(content)
                        # print('#' * 50)
                        for site in websites:
                            if site in content:
                                # print("site :: ",site)
                                # print("if part")
                                pass
                            else:
                                # print("else part")
                                file.write(redirect + " " + site + "\n")
                except:
                    pass
            else:
                if self.web_block:
                    break
                try:
                    with open(hostsPath, 'r+') as file:
                        content = file.readlines()
                        file.seek(0)
                        for line in content:
                            if not any(site in line for site in websites):
                                file.write(line)
                            file.truncate()
                    # print("Allowed access!")
                except:
                    pass
            time.sleep(5)

    # ##########################################################
    def showTime(self):
        # print("strating_time:############",self.string_time)
        if self.string_time == 'Time : 0:0:0':
            # print(":::: if block of showtime ::::")

            if self.time_start:
                data = self.Keyloger.write_time
                print("data in showTime if part ", data, self.time_count)
                self.time_1 = self.time_count
                cur_x = datetime.datetime.now()
                cur_x = int(cur_x.strftime("%H") + "" + cur_x.strftime("%M") + "" + cur_x.strftime("%S"))

                if (int(data) - int(cur_x)) != 0:
                    cur_x = str(cur_x)
                    cur_x = cur_x[4:]
                    data = str(data)
                    data = data[4:]

                    if ((int(data) == int(cur_x))):
                        print("time same")
                        self.time_count = self.time_count - 60

                    if int(cur_x) % 10 == 0:
                        total_time_send = self.time_formate
                        print("if block of show time total_time_send = self.time_formate ::: ", total_time_send)
                        # try:
                        #     with open('C:\\Users\\keyLog.txt', 'r') as read_key_logger_file:
                        #         key_logger = read_key_logger_file.read()
                        # except:
                        #     key_logger = ''

                        key_logger = self.Keyloger.Attendence_keyloger_multi_string
                        print("key_logger for attendence", key_logger)
                        print("key_logger for showtime", key_logger)
                        # URL = "http://localhost/customci3.1/Api/attendance"
                        # URL = "https://www.fineoutput.website/task_manager/employee/api/Home/attendance"
                        #
                        # headers = {
                        #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                        # # r = requests.post(url=URL, data={'email': 'demo@gmail.com', 'password': 123}, headers=headers)
                        # r = requests.post(url=URL, data={'email': self.email, 'password': self.password,
                        #                                  'key_logger': key_logger,
                        #                                  'total_time': total_time_send}, headers=headers)
                        # print(r)
                        # print(r.content)
                        # res = json.loads(r.text)

                self.time_count += 1
        else:

            if self.time_start:
                data = self.Keyloger.write_time
                # ########################################################
                self.time_1 = self.time_count
                cur_x = datetime.datetime.now()
                cur_x = int(cur_x.strftime("%H") + "" + cur_x.strftime("%M") + "" + cur_x.strftime("%S"))

                self.time_count += 1
                # print(" self.time_count = hour_in_sec+minute_in_sec+second_in_sec ",self.time_count)

                # ########################################################
                self.time_1 = self.time_count
                cur_x = datetime.datetime.now()
                cur_x = int(cur_x.strftime("%H") + "" + cur_x.strftime("%M") + "" + cur_x.strftime("%S"))

                # print('data :::', data)
                # print("cur_x :: ",cur_x)
                if (int(data) - int(cur_x)) != 0:
                    cur_x = str(cur_x)
                    cur_x = cur_x[4:]
                    data = str(data)
                    data = data[4:]

                    # if ((int(data) - int(cur_x))%60 == 0):
                    if ((int(data) == int(cur_x))):
                        print("time same")
                        self.time_count = self.time_count - 60
                # self.time_count += 1

        if self.time_start:
            text = self.time_count
            seconds = text % (24 * 3600)
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60

            if len(str(hour)) > 1:
                hour = str(hour)
            else:
                hour = '0' + str(hour)

            if len(str(minutes)) > 1:
                minutes = str(minutes)
            else:
                minutes = '0' + str(minutes)

            if len(str(seconds)) > 1:
                seconds = str(seconds)
            else:
                seconds = '0' + str(seconds)

            self.time_formate = f'Time : {hour}:{minutes}:{seconds}'
            self.time_label.setText(self.time_formate)

    def logout_ok_btn(self):
        print("logout_ok_btn yes")
        self.logout_dialog.hide()
        try:

            self.video_share_thread_stop = True
            self.client_thread_stop = True
            # del self.thread
            c_t_s = self.client_thread_stop
            self.thread_client.raise_exception()
            print("del client thread object before".upper(), self.thread_client)
            del self.thread_client

            self.thread.raise_exception()

            del self.thread

            # print("del client thread object before".upper(), self.thread_client)
            # ######################################################################
            self.timeer_flag = False
            self.time_start = False
            self.web_block = True
            self.time_count = 0
            self.web_block_flag = False

            self.count = 0
        except:
            print("Except ")
        # self.Keyloger.stop_threads = False
        try:
            total_time_send = self.time_formate
        except:
            total_time_send = 'Time : 00:00:00'

        try:
            split_time = total_time_send.split(":")
            # print("SPLIT TIME IS ::::: ",split_time)
            if len(split_time[1]) < 3:
                hour = split_time[1][: 1] + '0' + split_time[1][1:]
                print("need to edit time split_time[1] hour ::::::::::", hour)
            else:
                hour = split_time[1]
            if len(split_time[2]) < 2:
                minute = '0' + split_time[2]
                # print("need to edit time split_time[2] minute :::::::::: ",minute)
            else:
                minute = split_time[2]
            if len(split_time[3]) < 2:
                second = '0' + split_time[3]
                # print("need to edit time split_time[3] second :::::::::::",second)
            else:
                second = split_time[3]
            total_time_send = hour + ":" + minute + ":" + second
            # with open('C:\\Users\\keyLog.txt', 'r') as read_key_logger_file:
            #     key_logger = read_key_logger_file.read()
            key_logger = self.Keyloger.Attendence_keyloger_multi_string
            print("key_logger for attendence", key_logger)

            print("key_logger logout::::::::: ", key_logger)

            # URL = "http://localhost/customci3.1/Api/attendance"
            URL = "https://www.fineoutput.us/employee/api/Home/attendance"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

            r = requests.post(url=URL, data={'email': self.email, 'password': self.password, 'key_logger': key_logger,
                                             'total_time': total_time_send}, headers=headers)
            # res = json.loads(r.text)

            # self.stackedWidget.setCurrentWidget(self.settings_page)

            # ######################################################################

            self.thread_client = Client(c_t_s)
        except:
            pass
        # ############# Data base entry delete ############
        # def delete_database_entry(id):
        print("logout button email ", self.email)
        conn = sqlite3.connect("fineoutput_employee.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM employee WHERE email=?", (self.email,))
        conn.commit()
        conn.close()
        # #################################################
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def logout_cancel_btn(self):
        self.logout_dialog.hide()
        print("logout_ok_btn cancel")

    def logout(self):
        # ///////////////////////////////////////
        # self.logout_dialog
        self.logout_dialog = logout_dialog()
        self.logout_dialog.label.setText("Do You Want To Logout ? ")
        self.logout_dialog.label.setAlignment(QtCore.Qt.AlignCenter)
        self.logout_dialog.pushButton.clicked.connect(self.logout_ok_btn)
        self.logout_dialog.pushButton_2.clicked.connect(self.logout_cancel_btn)
        # ///////////////////////////////////////
        print("logout")
        # del self.thread_client


    def setting(self):
        self.home_button.setStyleSheet(css_not_active)
        self.screen_share.setStyleSheet(css_not_active)
        self.attendence_button.setStyleSheet(css_not_active)
        self.task_button.setStyleSheet(css_not_active)
        self.setting_button.setStyleSheet(css_active)
        print("setting button click")
        self.setting = Setting()

        self.setting.show()
        # widget.setCurrentIndex(widget.currentIndex() + 1)

    def pause(self):
        print("pause 0".upper())
        self.timeer_flag = False
        self.time_start = False
        self.resume_button.show()
        self.pause_button.hide()
        self.lunch_break_button_handle = 'pause'
        print("pause 1".upper())

    def resume(self):
        print("resume 0".upper())
        self.timeer_flag = True
        self.time_start = True
        self.resume_button.hide()
        self.pause_button.show()
        self.lunch_break_button_handle = 'resume'
        print("resume 1".upper())

    def attendence_stop_ok_btn_response(self):
        self.attendence_stop_dialog_responce_message.hide()

    def attendence_stop_ok_btn(self):
        self.attendence_stop_dialog.hide()
        print("attendence_stop_ok_btn ok button")

        #     /////////////////////////////////////////////
        self.timeer_flag = False
        self.time_start = False
        self.web_block = True
        self.time_count = 0
        self.web_block_flag = False
        self.start_button_flag = ""
        self.count = 0
        self.Keyloger.stop_threads = False

        total_time_send = self.time_formate
        split_time = total_time_send.split(":")
        # print("SPLIT TIME IS ::::: ",split_time)
        if len(split_time[1]) < 3:
            hour = split_time[1][: 1] + '0' + split_time[1][1:]
            # print("need to edit time split_time[1] hour ::::::::::",hour)
        else:
            hour = split_time[1]
        if len(split_time[2]) < 2:
            minute = '0' + split_time[2]
            # print("need to edit time split_time[2] minute :::::::::: ",minute)
        else:
            minute = split_time[2]
        if len(split_time[3]) < 2:
            second = '0' + split_time[3]
            # print("need to edit time split_time[3] second :::::::::::",second)
        else:
            second = split_time[3]
        total_time_send = hour + ":" + minute + ":" + second
        # with open('C:\\Users\\keyLog.txt', 'r') as read_key_logger_file:
        #     key_logger = read_key_logger_file.read()

        key_logger = self.Keyloger.Attendence_keyloger_multi_string
        print("key_logger for attendence", key_logger)
        print("key_logger Stop::::::::: ", key_logger)

        # URL = "http://localhost/customci3.1/Api/attendance"
        URL = "https://www.fineoutput.us/employee/api/Home/attendance"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        try:
            r = requests.post(url=URL, data={'email': self.email, 'password': self.password, 'key_logger': key_logger,
                                             'total_time': total_time_send}, headers=headers)
            res = json.loads(r.text)
            print(res)
            if r.status_code == 200:
                self.attendence_stop_dialog_responce_message = attendence_stop_dialog_responce_message()
                succ_mess = res['message'].title()
                self.attendence_stop_dialog_responce_message.label.setText(succ_mess)
                self.attendence_stop_dialog_responce_message.label.setAlignment(QtCore.Qt.AlignCenter)
                self.attendence_stop_dialog_responce_message.pushButton.clicked.connect(
                    self.attendence_stop_ok_btn_response)

            self.stackedWidget.setCurrentWidget(self.settings_page)
        except:
            print("attendence stopok btn except")

    def attendence_stop_cancel_btn(self):
        self.attendence_stop_dialog.hide()
        print("attendence_stop_cancel_btn cancel button")

    def stop(self):
        # ////////////////////////////////
        self.attendence_stop_dialog = attendence_stop_dialog()
        self.attendence_stop_dialog.label.setText("Do You Want To Stop Attendence Time ? ")
        self.attendence_stop_dialog.label.setAlignment(QtCore.Qt.AlignCenter)
        self.attendence_stop_dialog.pushButton_3.clicked.connect(self.attendence_stop_ok_btn)
        self.attendence_stop_dialog.pushButton_2.clicked.connect(self.attendence_stop_cancel_btn)
        # ////////////////////////////////


    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        # p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        p = convert_to_Qt_format.scaled(1300, 680, QtCore.Qt.KeepAspectRatio)

        return QPixmap.fromImage(p)


if __name__ == "__main__":
    Appp = QApplication(sys.argv)
    # mainwindow = Login()
    # connect_database()
    # print("ok database create")
    mainwindow = SplashScreen()

    widget = QtWidgets.QStackedWidget()
    widget.setGeometry(400, 100, 600, 415)
    widget.setWindowTitle("Fine output")
    widget.setWindowIcon(QtGui.QIcon('logo.png'))
    # widget.setWindowFlag(Qt.FramelessWindowHint, True)
    widget.addWidget(mainwindow)

    widget.show()
    Appp.exec_()
