class LinuxUser:

    def __init__(self, username, password, type, uid, gid):
        self.__username = username
        self.__password = password
        self.__type = type
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

    def get_type(self):
            return self.__type

    def set_type(self,type):
        self.__type = type

    def get_uid(self):
            return self.__uid

    def set_uid(self,uid):
        self.__uid = uid

    def get_gid(self):
            return self.__gid

    def set_gid(self,gid):
        self.__gid = gid

    def str(self):
        return "{}|{}|{}|{}|{}".format(self.get_username(),self.get_password(),self.get_type(),
            self.get_uid(),self.get_gid())

    def dict(self):

        response = {
            "username" : self.get_username(),
            "password" : self.get_password(),
            "type" : self.get_type(),
            "uid" : self.get_uid(),
            "gid" : self.get_gid()
        }

        return response
