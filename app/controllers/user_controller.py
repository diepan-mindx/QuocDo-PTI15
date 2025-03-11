import os
import sys

from models.user import User
from DAO import DAO

class UserController:
    def __init__(self):
        self.__user_list = []
        self.__generate_user_list()
        
    def get_user_list(self):
        return self.__user_list

    # private methods (only this class can use)
    def __generate_user_list(self):
        # get from data json
        self.__user_list = DAO.load_json_data("user")
        self.__convert_dict_to_objects()  # Convert dict list to User objects

    def __convert_dict_to_objects(self):
        self.__user_list = [User(user['email'], user['password'], user['username']) for user in self.__user_list]  # Convert each dict to user object

    def __convert_users_to_dict(self):
        return [{'email': user.get_email(), 'password': user.get_password(), 'username': user.get_username()} for user in self.__user_list]

    def __save_user_data(self):
        # save list for file data
        DAO.save_json_data("user", self.__convert_users_to_dict())

    # read
    def find_user_by_username(self, username):
        for user in self.__user_list:
            if user.get_username() == username:
                return user
        # user not found
        return None

    def find_user_by_email(self, email):
        for user in self.__user_list:
            if user.get_email() == email:
                return user
        return None

    # add
    def add_user(self, user: User):
        self.__user_list.append(user)
        self.__save_user_data()

    def remove_user_by_email(self, deleted_email: str):
        # update by email
        for i, user in enumerate(self.__user_list):
            if user.get_email() == deleted_email:
                self.__user_list.pop(i)
                self.__save_user_data()
                return

    # delete
    def delete_user(self, deleted_email: str):
        # delete by email
        for i, user in enumerate(self.__user_list):
            if user.get_email() == deleted_email:
                self.__user_list.pop(i)
                self.__save_user_data()
                return
    
    # sort---------------------------------------------------------------
    def sort_users_by_username(self):
        # function 1 line -> lambda
        get_username = lambda user: user.get_username()
        # key requires passing a function to return username when filtering through each user
        return self.__user_list.sort(key=get_username)

    def sort_users_by_email(self):
        # sort by email attribute (from A to Z), key is the criteria for comparison
        self.__user_list.sort(key=lambda user: user.get_email())
