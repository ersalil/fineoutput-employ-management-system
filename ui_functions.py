from main import CreateAcc
from PyQt5.QtCore import *
from PyQt5 import QtCore

class UIFunctions(CreateAcc):

    def toggleMenu(self, maxWidth, enable):
        if enable:
            print("toggle btn clicked")
            # GET WIDTH
            width = self.left_side_menu.width()
            width1 = self.left_menu_top_buttons.width()
            maxExtend = maxWidth
            standard = 43

            # SET MAX WIDTH
            if width == 250:
                print("1")
                widthExtended = standard
            else:
                print("3")
                widthExtended = maxExtend

            if width1 == 250:
                print("2")
                widthExtended1 = standard
            else:
                print("4")
                widthExtended1 = maxExtend

            print(widthExtended,width)
            # ANIMATION
            self.animation = QPropertyAnimation(self.left_side_menu, b"minimumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

            self.animation1 = QPropertyAnimation(self.left_menu_top_buttons, b"minimumWidth")
            self.animation1.setDuration(400)
            self.animation1.setStartValue(width1)
            self.animation1.setEndValue(widthExtended1)
            self.animation1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation1.start()



