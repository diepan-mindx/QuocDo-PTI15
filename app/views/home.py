from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6 import uic
from PyQt6.QtCore import QTimer, QFile, QTextStream
from models.scramble import Scramble
from controllers.user_controller import UserController
from controllers.history_controller import HistoryController
from models.history import History


class Home(QMainWindow):
    def __init__(self, root_ui_path, currentUserEmail):
        super().__init__()
        self.ui = uic.loadUi(root_ui_path + "home.ui", self)
        self.root_ui_path = root_ui_path
        self.currentUserEmail = currentUserEmail
        self.historyController = HistoryController()
        self.userController = UserController()
        self.timer = QTimer(self)
        self.timer.setInterval(100)

        self.show_best_and_worst()
        self.history_table.hide()  # Hide history table initially

        # Click event to confirm delete
        self.history_table.cellClicked.connect(self.confirm_delete_history)

        self.history_btn.clicked.connect(self.toggle_history)
        self.about_btn.clicked.connect(self.show_about)
        self.start_btn.clicked.connect(self.start_clock)
        self.stop_btn.clicked.connect(self.stop_clock)
        # Change setting button to mode button
        self.mode_btn.clicked.connect(self.toggle_theme)
        self.scramble_btn.clicked.connect(self.change_scramble)

        # Load the default theme (light mode)
        self.current_theme = "light"
        self.apply_theme(self.current_theme)

    def change_scramble(self):
        scramble_obj = Scramble(self.type_cb.currentText())
        scramble_text = scramble_obj.random_steps()
        self.scramble.setText(scramble_text)
        print("change scramble")

    def toggle_theme(self):
        """Toggle between Light and Dark theme."""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme(self.current_theme)

    def apply_theme(self, theme):
        """Apply a theme from a .qss file."""
        qss_file = f"{self.root_ui_path}{theme}.qss"
        file = QFile(qss_file)
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
            file.close()

    def show_setting(self):
        print("setting")

    def toggle_history(self):
        if not self.history_table.isVisible():
            self.load_history_items()
            self.history_table.show()
        else:
            self.history_table.hide()

    def show_about(self):
        from views.about import About

        try:
            if not hasattr(self, "about"):
                about = About(self.root_ui_path)
                about.show()
        except Exception as e:
            print(e)

    def start_clock(self):
        try:
            self.sec.setText("0")
            self.msec.setText("0")
            self.start_btn.setStyleSheet("background-color: green;")
            self.timer.timeout.connect(self.update_time)
            self.timer.start()
            self.update_time()
            self.start_btn.setEnabled(False)
        except Exception as e:
            print(e)

    def update_time(self):
        old_time = int(self.msec.text())
        new_time = old_time + 1
        sec_text = str(new_time // 10 + int(self.sec.text()))
        msec_text = str(new_time % 10)
        self.msec.setText(msec_text)
        self.sec.setText(sec_text)

    def stop_clock(self):
        try:
            self.start_btn.setStyleSheet("background-color: #012a4a;")
            self.start_btn.setEnabled(True)
            self.timer.stop()

            finish_time = f"{self.sec.text()}.{self.msec.text()}"
            new_history = History(
                0, finish_time, self.currentUserEmail, self.type_cb.currentText()
            )
            self.historyController.add_history(new_history)

            self.load_history_items()
            self.show_best_and_worst()
        except Exception as e:
            print(e)

    def show_best_and_worst(self):
        self.best.setText(
            f"Best: {self.historyController.find_best(self.currentUserEmail)}"
        )
        self.worst.setText(
            f"Worst: {self.historyController.find_worst(self.currentUserEmail)}"
        )

    def confirm_delete_history(self, row, column):
        """Show a confirmation dialog before deleting a history item by ID."""
        try:
            history_id = int(
                self.history_table.item(row, 0).text()
            )  # Get ID from column 2
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Delete Confirmation")
            msg_box.setText(
                f"Are you sure you want to delete history ID: {history_id}?"
            )
            msg_box.setStandardButtons(
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            msg_box.setIcon(QMessageBox.Icon.Warning)

            result = msg_box.exec()

            if result == QMessageBox.StandardButton.Yes:
                self.historyController.delete_history(history_id)
                self.load_history_items()  # Refresh table after deletion
        except Exception as e:
            print(f"Error deleting history: {e}")

    def load_history_items(self):
        """Load history data into the table, including ID."""
        try:
            history_list = self.historyController.search_by_creator(
                self.currentUserEmail
            )
            if history_list:
                self.history_table.setRowCount(len(history_list))  # Set row count
                for index, item in enumerate(history_list):
                    self.history_table.setItem(
                        index, 0, QTableWidgetItem(str(item.get_id()))
                    )  # Time
                    self.history_table.setItem(
                        index, 1, QTableWidgetItem(str(item.get_time()))
                    )  # Type
                    self.history_table.setItem(
                        index, 2, QTableWidgetItem(str(item.get_type()))
                    )  # ID (now visible)

        except Exception as e:
            print(e)
