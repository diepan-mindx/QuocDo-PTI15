from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic
import sys
import os


# tạo class để chứa giao diện login
class About(QMainWindow):
    def __init__(self, root_ui_path):
        super().__init__()
        # kết nối giao diện với code
        self.ui = uic.loadUi(root_ui_path + "about.ui", self)
