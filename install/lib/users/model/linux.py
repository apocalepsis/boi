class Implementation:

    def __init__(self, username, password, uid, gid):
        self.__username = username
        self.__password = password
        self.__uid = uid
        self.__gid = gid

    def get_username(self):
        return self.__username

    def set_username(self,username):
        self.__username = username

    def get_password(self):
            return self.__password

    def set_password(self,password):
        self.__password = password

    def get_uid(self):
            return self.__uid

    def set_uid(self,uid):
        self.__uid = uid

    def get_gid(self):
            return self.__gid

    def set_gid(self,gid):
        self.__gid = gid

    def str(self):
        return "{}|{}|{}|{}".format(self.get_username(),self.get_password(),
            self.get_uid(),self.get_gid())

    def dict(self):

        response = {
            "username" : self.get_username(),
            "password" : self.get_password(),
            "uid" : self.get_uid(),
            "gid" : self.get_gid()
        }

        return response
