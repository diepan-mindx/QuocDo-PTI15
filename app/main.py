import sys
import os
from PyQt6.QtWidgets import QApplication
from views.login import Login
from views.home import Home


if __name__ == '__main__':
    app = QApplication(sys.argv)
    root_ui_path = 'app/ui/'
    login = Login(root_ui_path)
    login.show()
    sys.exit(app.exec())