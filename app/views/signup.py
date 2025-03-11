import sys
import os
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt6 import uic

from models.user import User
from controllers.user_controller import UserController


class Signup(QMainWindow):
    def __init__(self, root_ui_path):
        super().__init__()
        self.root_ui_path = root_ui_path
        uic.loadUi(root_ui_path + "signup.ui", self)
        self.setWindowTitle("Sign Up")

        # Initialize UserController
        self.userController = UserController()

        try:
            self.signup_btn.mousePressEvent = self.register_user
            self.login_btn.mousePressEvent = self.open_login
        except Exception as e:
            print(f"Error: {e}")

    def register_user(self, event):
        from views.login import Login  # Import Login instead of Home

        email = self.email.text()
        password = self.password.text()
        confirm_password = self.confirmPassword.text()

        # Validation
        if not (email and password and confirm_password):
            self.show_error("Vui lòng điền đầy đủ thông tin đăng ký!")
            return

        if password != confirm_password:
            self.show_error("Mật khẩu xác nhận không khớp!")
            return

        try:
            # Check if the email is already registered
            existingUserByEmail = self.userController.find_user_by_email(email)

            if existingUserByEmail:
                self.show_error("Email đã được sử dụng, vui lòng chọn email khác!")
                return

            # Create new user
            new_user = User(email=email, password=password)
            self.userController.add_user(new_user)

            # Registration successful, open Login window
            try:
                login_window = Login(self.root_ui_path)  # Open login window
                login_window.show()
            except Exception as e:
                self.show_error("Failed to open login window: " + str(e))

            self.close()  # Close signup window
        except Exception as e:
            print("Error signup", e)

    def open_login(self, event):
        from views.login import Login

        try:
            login_window = Login(self.root_ui_path)
            login_window.show()
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
