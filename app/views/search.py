from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6 import uic
from controllers.user_controller import UserController
import sys
from controllers.note_controller import NoteController


class Search(QMainWindow):
    def __init__(self, root_ui_path, search_key):
        super(Search, self).__init__()
        self.ui = uic.loadUi(root_ui_path + "search.ui", self)

        self.search_key = search_key
        self.note_controller = NoteController()
        # gan danh sach sau khi tim kiem cho list_item
        self.setListItem()

        # bat su kien cho cac button
        self.ui.edit_btn.clicked.connect(self.edit)
        self.ui.create_btn.clicked.connect(self.create)
        self.ui.delete_btn.clicked.connect(self.delete)
        self.ui.cancel_btn.clicked.connect(self.cancel)
        self.ui.list_item.itemClicked.connect(self.on_item_clicked)
    def setCurrentItemDAtaFrom(self,item_clicked):
        full_item_data = self.note_controller.search_by_title(item_clicked)
        self.ui.name_inp.setText(full_item_data.name)
        self.ui.created_by_inp.setText(full_item_data.created_by)
        self.ui.note_inp.setText(full_item_data.note)

    def setListItem(self):
        # lay list tu data
        result_list = self.note_controller.search_by_title(self.search_key)
        # kiem tra neu co danh sach
        if result_list:
            # loc ra thuoc tinh ten cho danh sach
            list_name = [i.title for i in result_list]
            # add danh sach vao list widget
            self.ui.list_item.addItems(list_name)
        else:
            self.show_message("Khong tim thay du lieu phu hop")

    def edit(self):
        self.isEdit = True
        # lay duoc hang dang duoc chon
        current_data = self.ui.list_item.currentItem()
        # lay full du lieu thong qua name
        full_current_object = self.note_controller.search_by_title(current_data)
        # load du lieu cu len edit form
        self.ui.name_inp.setText(full_current_object.name)
        self.ui.created_by_inp.setText(full_current_object.created_by)
        self.ui.note_inp.setText(full_current_object.note)

    def create(self):
        # lay lai du lieu tu form input
        name_inp = self.ui.name_inp.text()
        created_by_inp = self.ui.created_by_inp.text()
        note_inp = self.ui.note_inp.text()
        # tao object luu du lieu trong input
        full_input_object = {}

        # validate form
        if not (name_inp and created_by_inp and note_inp):
            self.show_message("Vui long nhap du form")
            return # khong lam gi them 
        
        # luu du lieu => edit
        if self.isEdit:
            self.history_controller.update_note(full_input_object)
        else:
            # luu duoi dang create
            self.history_controller.add_note(full_input_object)
            
    def delete(self):
        current_data = self.ui.list_item.currentItem()
        full_current_object = self.note_controller.search_by_title(current_data)
        msg_box = QMessageBox
        msg_box.setWindowTitle('warning')
        msg_box.setText('ban co chac muon xoa du lieu nay')
        msg_box.setIcon(QMessageBox.Icon.Warning)
        ok_button = msg_box.addButton(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        ok_button.setStyleSheet('background_color: #598896;')
        response = msg_box.exec()
        if  response == QMessageBox.StandardButton.No:
            return
        elif response == QMessageBox.StandardButton.Yes:
            self.history_controller.delete_note(full_current_object)
            self.setListItem
        

    def cancel(self):
        self.ui.name_inp.setText('')
        self.ui.created_by_inp.setText('')
        self.ui.note_inp.setText('')

    def show_message(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Message")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        ok_button = msg_box.addButton(QMessageBox.StandardButton.Ok)
        ok_button.setStyleSheet("background-color: #598896;")
        msg_box.exec()