class Implementation:

    def __init__(self, username, password, salt):
        self.__username = username
        self.__password = password
        self.__salt = salt

    def get_username(self):
        return self.__username

    def set_username(self,username):
        self.__username = username

    def get_password(self):
            return self.__password

    def set_password(self,password):
        self.__password = password

    def get_salt(self):
            return self.__salt

    def set_salt(self,salt):
        self.__salt = salt

    def str(self):
        return "{}|{}|{}".format(self.get_username(),self.get_password(),self.get_salt())

    def dict(self):

        response = {
            "username" : self.get_username(),
            "password" : self.get_password(),
            "salt" : self.get_salt()
        }

        return response
