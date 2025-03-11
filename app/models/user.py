class User:
    # khai bao thuoc tinh can cho object user
    def __init__(self, email, password, username='default'):
        self.__email = email
        self.__password = password
        self.__username = username

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password

    def set_username(self, username):
        self.__username = username

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def get_username(self):
        return self.__username

    def __str__(self):
        return f"Username: {self.__username}, Email: {self.__email}, Password: {self.__password}"