class User:

    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    def get_username(self):
        return self.__username

    def set_username(self,username):
        self.__username = username

    def get_password(self):
            return self.__password

    def set_password(self,password):
        self.__password = password

    def __str__(self):
        return "{}|{}".format(self.get_username(),self.get_password())
