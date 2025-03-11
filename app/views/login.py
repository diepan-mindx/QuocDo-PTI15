import sys
import os
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt6 import uic

from models.user import User
from controllers.user_controller import UserController


class Login(QMainWindow):
    def __init__(self, root_ui_path):
        super().__init__()
        self.root_ui_path = root_ui_path
        uic.loadUi(root_ui_path + "login.ui", self)
        self.setWindowTitle("Log In")
        # Initialize UserController
        self.userController = UserController()

        try:
            self.login_btn.mousePressEvent = self.check_login
            self.signup_btn.mousePressEvent = self.open_signup
        except Exception as e:
            print(f"Error: {e}")

    def check_login(self, event):
        from views.home import Home

        email = self.email.text()
        password = self.password.text()

        # Validation for email and password
        if not (email and password):
            self.show_error("Vui lòng điền đầy đủ thông tin đăng nhập!")
            return
        try:
            # Check if the account exists in the system
            currentUser = self.userController.find_user_by_email(email)

            if not currentUser:
                self.show_error("Tài khoản chưa tồn tại, vui lòng đăng ký!")
                return
            else:
                # Check password
                if currentUser.get_password() == password:
                    # Login successful
                    try:
                        home = Home(
                            self.root_ui_path, currentUser.get_username()
                        )
                        home.show()
                    except Exception as e:
                        print("Failed to open home window: " + str(e))

                    self.close()
                else:
                    # Incorrect password
                    self.show_error("Thông tin đăng nhập không chính xác!")
                    return
        except Exception as e:
            print("Error login", e)

    def open_signup(self, event):
        from views.signup import Signup

        try:
            signup_window = Signup(self.root_ui_path)  # Updated to use Signup
            signup_window.show()
            self.close()
        except Exception as e:
            print(e)

    def show_error(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        ok_button = msg_box.addButton(QMessageBox.StandardButton.Ok)
        ok_button.setStyleSheet("background-color: #598896;")
        msg_box.exec()