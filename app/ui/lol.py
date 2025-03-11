from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtCore import QPropertyAnimation, QRect
from PyQt6.QtGui import QColor

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login UI")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #1E1E2E;")

        layout = QVBoxLayout(self)

        # Tạo nút đăng nhập
        self.login_button = QPushButton("Đăng nhập", self)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #8CAAEE;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        self.login_button.setFixedSize(150, 50)
        
        layout.addWidget(self.login_button)

        # Thêm hiệu ứng động
        self.init_animations()

    def init_animations(self):
        """ Khởi tạo hiệu ứng động cho nút """
        self.login_button.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.login_button:
            if event.type().name == "Enter":  # Khi di chuột vào
                self.animate_button(1.1, "#6B8BC3")
            elif event.type().name == "Leave":  # Khi di chuột ra
                self.animate_button(1.0, "#8CAAEE")
        return super().eventFilter(obj, event)

    def animate_button(self, scale_factor, color):
        """ Hiệu ứng phóng to & đổi màu """
        # Animation kích thước
        anim = QPropertyAnimation(self.login_button, b"geometry")
        anim.setDuration(200)
        current_rect = self.login_button.geometry()
        new_rect = QRect(current_rect.x(), current_rect.y(),
                         int(150 * scale_factor), int(50 * scale_factor))
        anim.setStartValue(current_rect)
        anim.setEndValue(new_rect)
        anim.start()

        # Cập nhật màu sắc động bằng stylesheet
        self.login_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 10px;
                transition: background-color 0.3s ease-in-out;
            }}
        """)

# Chạy ứng dụng
app = QApplication([])
window = LoginWindow()
window.show()
app.exec()
