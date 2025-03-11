class History:
    # khai bao thuoc tinh can cho object history
    def __init__(self, id, time, created_by, type_name):
        self.__id = id
        self.__time = time
        self.__created_by = created_by
        self.__type = type_name

    def set_id(self, id):
        self.__id = id

    def set_time(self, time):
        self.__time = time

    def set_created_by(self, created_by):
        self.__created_by = created_by

    def set_type(self, type):
        self.__type = type

    def get_id(self):
        return self.__id

    def get_time(self):
        return self.__time

    def get_created_by(self):
        return self.__created_by

    def get_type(self):
        return self.__type

    def __str__(self):
        return f"ID: {self.__id}, Time: {self.__time}, Created By: {self.__created_by}, Type: {self.__type}"
